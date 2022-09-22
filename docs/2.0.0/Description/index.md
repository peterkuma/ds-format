---
layout: default
title: Description
---

## Description

Below is a high-level description of the Python interface provided by ds for
reading and writing data files. The general structure of the ds format is:

```python
# Dataset definition:
d = {
    # Variable 1 (NumPy array or list):
    "<var1>": [...],
    # Variable 2 (NumPy array or list):
    "<var2>": [...],
    ...,
    # Metadata:
    ".": {
        # Variable 1 metadata:
        "<var1>": { 
            # Dimension names:
            ".dims": ["<dim1>", "<dim2>", ...],
            # Arbitrary attributes:
            "<attr1>": ...,
            "<attr2>": ...,
            ...
        },
        # Variable 2 metadata:
        "<var2>": {
            # Dimension names:
            ".dims": ["<dim1>", "<dim2>", ...],
            # Arbitrary attributes:
            "<attr1>": ...,
            "<attr2>": ...,
            ...
        },
        ...
        # Dataset metadata:
        ".": {
            # Arbitrary attributes
            "<attr1>": ...,
            "<attr2>": ...,
            ...
        }
    }
}
```

where `d['<var<n>>']` are variables containing multi-dimensional
[NumPy](https://www.numpy.org/) arrays or Python lists, and `d['.']` stores the
metadata. `d['.']['<var<n>>']` contain
metadata of each variable – dimension names `.dims` and any number of
arbitrary variable-level attributes. `d['.']['.']` contains any number of
arbitrary dataset-level attributes. Groups and nesting of variables,
as implemented in HDF5, is currently not supported.

### Elements

#### Variables

Variables are multi-dimentional arrays with an arbitrary name, except for
names beginning with `.`, which have a special meaning.
The dimensions of variables are specified in the `.dims` list in the metadata.

#### Dimensions

Dimensions are names corresponding to dimensions of variables.
Dimensions can have the same name as another variable, which may then be
interpreted as the axis in certain programs such as
[Panoply](https://www.giss.nasa.gov/tools/panoply/), as is common in NetCDF
datasets.

#### Attributes

Attributes are objects defining variable or dataset metadata,
and can be arbitrary key-value pairs.

### Example

#### Using ds interface

This is an example of two variables `time` and `temperature` stored
in a dataset along with their metadata.

Using the command line interface:

```sh
ds write dataset.nc \
    { time time { 1 2 3 } } \
    { temperature time { 16. 18. 21. } units: degree_celsius } \
    title: "Temperature data"
```

Using the Python interface:

```python
import numpy as np
import ds_format as ds
d = {
    # Variable "time":
    'time': [1, 2, 3],
    # Variable "temperature":
    'temperature': [16., 18., 21.],
    '.': {
        '.': { 'title': 'Temperature data' },
        # Metadata of variable "time":
        'time': {
            # Single dimension named "time":
            '.dims': ['time'],
        },
        # Metadata of variable "temperature":
        'temperature': {
            # Single dimension named "time"
            '.dims': ['time'],
            # Arbitray attributes:
            'units': 'degree_celsius',
        },
    }
}
# Save the dataset as NetCDF:
ds.write('dataset.nc', d)
```

#### Using netCDF4 interface

The code produces an equivalent data file using the interface of the Python library
[netCDF4](http://unidata.github.io/netcdf4-python/):

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

The result can be viewed by `ncdump dataset.nc`:

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
