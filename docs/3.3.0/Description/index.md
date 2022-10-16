---
layout: default
title: Description
---

## Description

The ds format is both a data structure with a representation in a programming
language such as Python and a [storage format](../Storage_format/). In Python,
the ds format is a nested dictionary structure containing data and metadata,
which can be represented schematically as:

```python
d = {
    # Variable 1 data (NumPy ndarray, a list, or a scalar):
    '<var1>': ...,
    # Variable 2 data (NumPy ndarray, a list, or a scalar):
    '<var2>': ...,
    ...,
    # Metadata.
    '.': {
        # Variable 1 metadata:
        '<var1>': {
            # Variable 1 dimensions.
            '.dims': ['<dim>', ...],
            # Variable 1 size..
            '.size': [<size>, ...],
            # Variable 1 type.
            '.type': '<type>',
            # Variable 1 attributes.
            '<attr>': ...,
            ...
        },
        # Variable 2 metadata.
        '<var2>': {
            # Variable 2 dimensions.
            '.dims': ['<dim>', ...],
            # Variable 2 size..
            '.size': [<size>, ...],
            # Variable 2 type.
            '.type': '<type>',
            # Variable 2 attributes.
            '<attr>': ...,
            ...
        },
        ...
        # Dataset metadata.
        '.': {
            # Dataset attributes.
            '<attr>': ...,
            ...
        }
    }
}
```

`d['<var<n>>']` contain variable data as a [NumPy](https://www.numpy.org/)
array or Python list. `d['.']` contains metadata, `d['.']['<var<n>>']` contains
variable metadata and `d['.']['.']` contains dataset metadata.

The structure can be manipulated either directly or through the
[Python API](../Python_API/), which provides convenience functions over direct
manipulation. The data and metadata can be saved as NetCDF, HDF5,
[DS](../Storage_format), JSON and CSV with
**[ds.write](../Python_API/#write)**, and loaded from NetCDF, HDF5,
[DS](../Storage_format), JSON and CSV with **[ds.read](../Python_API/#read)**.

### Definition

#### Dataset

A dataset is a dictionary containing variable data and metadata.

Keys beginning with a dot (`.`) have a special meaning.  To suppress a special
meaning, names beginning with a dot and a backslash (`\`)
have to be escaped with a backslash (prepended with a backslash).

#### Variable data

Variable data are a multi-dimentional array (NumPy ndarray or MaskedArray, or
a Python `list`), or a scalar (`int`, `float`, `str`, `bytes` and `bool`). They
are stored in the dataset under arbitrary string keys, but names beginning with
a dot (`.`) or a backslash (`\`) have to be escaped (see above).

#### Metadata

Metadata is a dictionary containing variable metadata and dataset metadata.
Metadata are stored in the dataset under a key `.`.

#### Variable metadata

Variable metadata consist of variable attributes, and optionally of variable
dimensions (`.dims`), size (`.size`) and type (`.type`).

#### Variable dimensions

Variable dimensions is a list of names corresponding to the dimensions of the
variable data. The names can be arbitrary strings. Variable dimensions are
stored in variable metadata under a key `.dims`. For scalar and empty
variables, variable dimensions are an empty list (`[]`).

Dimensions can have the same name as another variable, which is then be
interpreted as the axis in certain programs such as
[Panoply](https://www.giss.nasa.gov/tools/panoply/), as is conventional in
NetCDF datasets.

#### Variable size

Variable size is a list of sizes of each dimension of the variable data. It
is populated by **[ds.read](../Python_API/#read)** when reading a dataset
from a file. Variable size is stored in a key `.size` in the variable metadata.
Variable data size takes precedence over `.size` if variable data are defined.
For scalar variables, variable size is an empty list (`[]`). For empty
variables, variable size is `None`.

#### Variable type

Variable type is a string specifying the data type.  It is populated by
**[ds.read](../Python_API/#read)** when reading a dataset from a file.
Variable type is stored in a key `.type` in the variable metadata. Variable
data type takes precedence over `.type` if variable data are defined.

#### Variable and dataset attributes

Attributes are objects defining variable or dataset metadata, and can be
arbitrary key–value pairs, where key is a string.

### Example

#### Using the ds interface

This is an example of two variables `time` and `temperature` stored
in a dataset along with their metadata.

Using the command line interface:

```sh
ds set { time none time { 1 2 3 } } \
       { temperature none time { 16. 18. 21. } units: degree_celsius } \
       title: "Temperature data" \
       none dataset.nc
```

Using the Python interface:

```python
import numpy as np
import ds_format as ds

d = {
    'time': [1, 2, 3],
    'temperature': [16., 18., 21.],
    '.': {
        '.': { 'title': 'Temperature data' },
        'time': {
            '.dims': ['time'],
        },
        'temperature': {
            '.dims': ['time'],
            'units': 'degree_celsius',
        },
    }
}
ds.write('dataset.nc', d)
```

The result can be viewed with `ds meta dataset.nc`:

{% raw %}
```
.: {{
	title: "Temperature data"
}}
temperature: {{
	units: degree_celsius
	.dims: { time }
	.size: { 3 }
	.type: float64
}}
time: {{
	.dims: { time }
	.size: { 3 }
	.type: int64
}}
```
{% endraw %}

and `ds cat time temperature dataset.nc`:

```
time temperature
1 16.000000
2 18.000000
3 21.000000
```

#### Using the netCDF4 interface

The code produces an equivalent data file using the interface of the Python
library [netCDF4](http://unidata.github.io/netcdf4-python/):

```python
import numpy as np
from netCDF4 import Dataset

d = Dataset('dataset.nc', 'w')
d.title = 'Temperature dataset'
d.createDimension('time', 3)
time = d.createVariable('time', 'i8', ('time',))
temperature = d.createVariable('temperature', 'f8', ('time',))
temperature.units = 'degree_celsius'
time[:] = np.array([1, 2, 3])
temperature[:] = np.array([16., 18., 21.])
d.close()
```

The result can be viewed with `ncdump dataset.nc`:

```
netcdf dataset {
dimensions:
    time = 3 ;
variables:
    int64 time(time) ;
    double temperature(time) ;
        temperature:units = "degree_celsius" ;

// global attributes:
        :title = "Temperature dataset" ;
data:

 time = 1, 2, 3 ;

 temperature = 16, 18, 21 ;
}
```
