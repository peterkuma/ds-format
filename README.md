# ds-python (beta)

ds-python is a Python implementation of a dataset format *DS* for storing data
along with metadata, similar to [NetCDF](https://www.unidata.ucar.edu/software/netcdf/)
and [HDF](https://www.hdfgroup.org). DS is based on
[JSON](https://json.org/)-like data structures common in
in high-level programming languages. It supports a subset
of functionality of NetCDF and is compatible with most existing NetCDF
datasets and the [CF Conventions](http://cfconventions.org/) (if the necessary
attributes are defined in the dataset).

This package contains the command line program **ds** and Python library
**ds_format**, which implement reading, writing and editing of datasets.
The library is designed so that functions are completely separated
from data (unlike in object oriented programming), which is more transparent
and faster, especially when working with large datasets.

Similar packages are [nco](http://nco.sourceforge.net/) (netCDF Operator),
[CDO](https://code.mpimet.mpg.de/projects/cdo/) (Climate Data Operator),
[xarray](https://xarray.pydata.org),
[iris](http://scitools.org.uk/iris/docs/latest/). Compatible programs
for viewing datasets include
[ncdump](https://www.unidata.ucar.edu/software/netcdf/),
[HDFView](https://www.hdfgroup.org/downloads/hdfview/) and
[Panoply](https://www.giss.nasa.gov/tools/panoply/).

## Format description

The general structure of the format is:

```python
d = { # Dataset definition
    "<var1>": [...], # Variable 1 (multi-dimensional array)
    "<var2>": [...], # Variable 2 (multi-dimensional array)
    ...,
    ".": { # Metadata
        "<var1>": { # Variable 1 metadata
            ".dims": ["<dim1>", "<dim2>", ...], # Dimension names
            "<attr1>": ..., # Arbitrary attributes
            "<attr2>": ...,
            ...
        },
        "<var2>": { # Variable 2 metadata
            ".dims": ["<dim1>", "<dim2>", ...], # Dimension names
            "<attr1>": ..., # Arbitrary attributes
            "<attr2>": ...,
            ...
        },
        ...
        ".": { # Dataset metadata
            "<attr1>": ..., # Arbitrary attributes
            "<attr2>": ...,
            ...
        }
    }
}
```

where `d['<var<n>>']` are variables containing multi-dimensional
[NumPy](https://www.numpy.org/) arrays, and `d['.']` stores the metadata.
`d['.']['<var<n>>']` contain
metadata of each variable: dimension names `.dims` and
arbitrary variable-level attributes. `d['.']['.']` contains arbitrary
dataset-level attributes.

### Elements

#### Variables

Variables are multi-dimentional arrays with an arbitrary name (except for
names beginning with `.`).
The dimensions of variables are named in the `.dims` array in the metadata.

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

This is an example of two variables `time` and `temperature` stored
in a dataset along with their metadata: 

```python
import numpy as np
import ds_format as ds
d = {
	'time': np.array([1, 2, 3]), # Variable "time" (numpy array)
	'temperature': np.array([16., 18., 21.]), # Variable "temperature" (numpy array)
	'.': {
		'.': { 'title': 'Temperature data' },
		'time': { # Metadata of variable "time"
			'.dims': ['time'], # Single dimension named "time"
		},
		'temperature': { # Metadata of variable "temperature"
			'.dims': ['time'], # Single dimension named "time"
			'units': 'degree_celsius', # Arbitray attributes
		},
	}
}
ds.write('dataset.nc', d) # Save the dataset as NetCDF
```

The corresponding [netCDF4](http://unidata.github.io/netcdf4-python/)
code is:

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

## Installation

Requirements:

- Python 2.7, Python 3, or a Python distribution such
as [Anaconda](https://www.anaconda.com/distribution/)

Required Python packages:

- [netCDF4](http://unidata.github.io/netcdf4-python/netCDF4/index.html)
- [Aquarius Time](https://github.com/peterkuma/aquarius-time)
- [pst](https://github.com/peterkuma/pst)

To install the required Python packages (use `pip3` instead of `pip` to
install with Python 3, append `--user` to install in home directory):

```sh
pip install netCDF4 https://github.com/peterkuma/aquarius-time/archive/master.zip https://github.com/peterkuma/pst/archive/master.zip
```

To install ds-python:

```
pip install https://github.com/peterkuma/ds-python/archive/master.zip
```

## Command line interface

### Synopsis

```sh
ds [<cmd>] [<options>...]
```

### Commands

| Command | Description |
| --- | --- |
| [*default*](#default) | List variables. |
| [cat](#cat) | Print variable. |
| [get](#get) | Get attribute at a path. |
| [merge](#merge) | Merge files along a dimension. |
| [meta](#meta) | Print metadata. |
| [select](#select) | Select and subset variables. |
| [stats](#stats) | Print variable statistics. |

#### *default*

```sh
ds [-l] <input>...
ds ls [-l] <input>... # Alias
```

List variables.

Arguments:

- `-l` - Print a detailed list.
- `input` - Input file.

Examples:

```sh
$ ds dataset.nc
temperature
time

$ ds -l dataset.nc
temperature(time=3)
time(time=3)
```

#### cat

```sh
ds cat [-h] [--jd] <var>[,<var>]... <input>
```

Print variable.

Arguments:

- `-h` - Print human-readable values.
- `--jd` - Convert time variables to Julian dates
    (see [Aquarius Time](https://github.com/peterkuma/aquarius-time)).
- `var` - Variable name.
- `input` - Input file.

Examples:

```sh
$ ds cat temperature dataset.nc
16.0
18.0
21.0
```

#### get

```sh
ds get <path> <input>
```

Get attribute at path.

Arguments:

- `path` - Attribute path.
- `input` - Input file.

#### merge

```sh
ds merge <dim> <input>... <output>
```

Merge files along a dimension.

Arugments:

- `dim` - Dimension name.
- `input` - Input file.
- `output` - Output file.

#### meta

```sh
ds meta <input>
```

Print metadata. The output is JSON-formatted.

- `input` - Input file.

Examples:

```sh
$ ds dataset.nc
{
    ".": {
        "title": "Temperature dataset"
    },
    "temperature": {
        ".dims": [
            "time"
        ],
        ".size": [
            3
        ],
        "units": "degree_celsius"
    },
    "time": {
        ".dims": [
            "time"
        ],
        ".size": [
            3
        ]
    }
}
```

#### select

```sh
ds select <input> <output> [<variables>] [sel: <sel>]
```

Select and subset variables.

Arguments:

- `input` - Input file.
- `output` - Output file.
- `variables` - List of variables (`{ var1 var2 ... }`) or `none` for all.
    Default: `none`.
- `sel` - Selector. Format: `{ <dim1>: <idx1> <dim2>: <idx2> ... }`,
    where `<dim<n>>` is dimension name and `<idx<n>>` is a list of indexes
    `{ <i1> <i2> ... }`.

#### stats

```sh
ds stats <var> <input>
```

Print variable statistics. The output is JSON-formatted.

Arguments:

- `var` - Variable name.
- `input` - Input file.

Output:

- `count` - Number of array elements.
- `max` - Maximum value.
- `mean` - Sample mean.
- `median` - Sample median.
- `min` - Minimum value.

Examples:

```sh
$ ds stats temperature dataset.nc
{
    "count": 3,
    "max": 21.0,
    "mean": 18.333333333333332,
    "median": 18.0,
    "min": 16.0
}
```

## Python interface

| Function | Description |
| --- | --- |
| [get_dims](#get_dims) | Get all dimension names in a dataset. |
| [get_vars](#get_vars) | Get all variable names in a dataset. |
| [merge](#merge) | Merge datasets along a dimension. |
| [read](#read) | Read dataset from a file. |
| [rename](#rename) | Rename a variable. |
| [select](#select) | Filter dataset by a selector. |
| [to_netcdf](#to_netcdf) | Write dataset to a NetCDF file. |
| [write](#write) | Write dataset to a file. |

To import the library:

```python
import ds_format as ds
```

### Functions

#### get_dims

```python
ds.get_dims(d)
```

Get all dimension names in a dataset.

Arguments:

- `d` - Dataset (dict).

Returns dimension names (list of str).

#### get_vars

```python
ds.get_vars(d)
```

Get all variable names in a dataset.

Arguments:

- `d` - Dataset (dict).

Returns variable names (list of str).

#### merge

```python
ds.merge(dd, dim, new=False)
```

Merge datasets along a dimension. Variables with incompatible dimensions
will contain the first value encountered.

Arguments:

- `dd` - Datasets (list of dict).
- `dim` - Name of dimension (str).
- `new` - Merge datasets along a new dimension (str).

Returns a dataset (dict).

#### read

```python
ds.read(filename, variables=None, sel=None, full=False, jd=False)
```

Read dataset from a file.

Arguments:

- `filename` - Filename (str).
- `variables` - Variable names to read (list of str).
- `sel` - Selector (see **select**).
- `full` - Read all metadata (bool).
- `jd` - Convert time variables to Julian dates
    (see [Aquarius Time](https://github.com/peterkuma/aquarius-time)) (bool).

Supported formats:

- NetCDF4 (`.nc`)

Returns dataset (dict).

#### rename

```python
ds.rename(d, old, new)
```

Rename a variable.

Arguments:

- `d` - Dataset (dict).
- `old` - Old variable name (str).
- `new` - New variable name (str).

Returns None.

#### select

```python
ds.select(d, sel)
```

Filter dataset by a selector.

Arguments:

- `d` - Dataset (dict).
- `sel` - Selector (dict).

Selector is a dictionary where each key is a dimension name and value
is a mask to apply along the dimension or a list of indexes.

Returns None.

#### to_netcdf

```python
ds.to_netcdf(filename, d)
```

Write dataset to a NetCDF file.

Arguments:

- `filename` - Filename (str).
- `d` - Dataset (dict).

Returns None.

#### write

```python
ds.write(filename, d)
```

Write dataset to a file. The file type is determined from the file extension.

Arguments:

- `filename` - Filename (str).
- `d` - Dataset (dict).

Supported formats:

- NetCDF4 (`.nc`)

Returns None.

## License

This software can be used, shared and  modified freely under the terms of
the MIT license. See [LICENSE.md](LICENSE.md).
