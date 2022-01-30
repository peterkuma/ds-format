# ds-format

ds-format is a Python implementation of a dataset format *DS* for storing data
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
in a dataset along with their metadata.

Command line:

```sh
ds write dataset.nc { time time { 1 2 3 } } { temperature time { 16. 18. 21. } units: degree_celsius } title: "Temperature data"
```

Python:

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

[netCDF4](http://unidata.github.io/netcdf4-python/) code:

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

Installation on Linux is recommended.

Requirements:

- Python 3, or a Python distribution such
as [Anaconda](https://www.anaconda.com/distribution/)

Required Python packages:

- [netCDF4](http://unidata.github.io/netcdf4-python/netCDF4/index.html)
- [Aquarius Time](https://github.com/peterkuma/aquarius-time)
- [pst](https://github.com/peterkuma/pst)

Install ds-format and dependencies with:

```
pip3 install ds-format
```

**Note:** Append `--user` to install in your home directory on unix-like
operating systems (make sure `~/.local/bin` is included in the PATH
environmental variable).

## Command line interface

### Synopsis

```sh
ds [<cmd>] [<options>...]
```

The command line interface is based on the [PST format](https://github.com/peterkuma/pst).

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
| [write](#write) | Write dataset to a file. |

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
# Print list variables in dataset.nc
$ ds dataset.nc
temperature
time

# Print detailed list of variables in dataset.nc
$ ds -l dataset.nc
temperature(time=3)
time(time=3)
```

#### cat

```sh
ds cat [-h] [--jd] <var> <input>
ds cat [-h] [--jd] { <var> <var> ... } <input>
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
# Print temperature values in dataset.nc
$ ds cat temperature dataset.nc
16.0
18.0
21.0
```

```sh
# Print time and temperature values in dataset.nc
$ ds cat { time temperature } dataset.nc
1,16.0
2,18.0
3,21.0
4,23.0
5,25.0
6,28.0
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
ds merge <dim> <input>... <output> [new: <new>] [variables: { <var>... }]
```

Merge datasets along a dimension `dim`. If the dimension is not defined in the
dataset, merge along a new dimension `dim`. If `new` is `none` and `dim` is not
new, variables without the dimension are set with the first occurrence of the
variable. If `new` is not `none` and `dim` is not new, variables without the
dimension `dim` are merged along a new dimension `new`. If `variables` is not
`none`, only those variables are merged along a new dimension and other
variables are set to the first occurrence of the variable.

Arugments:

- `dim` - Name of a dimension to merge along.
- `input` - Input file.
- `output` - Output file.

Options:

- `new` - Name of a new dimension.
- `variables` - Variables to merge along a new dimension or `none` for all
variables.

Examples:

```sh
# Write example data to dataset1.nc
$ ds write dataset1.nc { time time { 1 2 3 } } { temperature time { 16. 18. 21. } units: degree_celsius } title: "Temperature data"
# Write example data to dataset2.nc
$ ds write dataset2.nc { time time { 4 5 6 } } { temperature time { 23. 25. 28. } units: degree_celsius } title: "Temperature data"
# Merge dataset1.nc and dataset2.nc and write the result to dataset.nc
$ ds merge time dataset1.nc dataset2.nc dataset.nc
# Print time and temperature variables in dataset.nc
$ ds cat { time temperature } dataset.nc
1,16.0
2,18.0
3,21.0
4,23.0
5,25.0
6,28.0
```

#### meta

```sh
ds meta <input>
```

Print metadata. The output is JSON-formatted.

- `input` - Input file.

Examples:

```sh
# Print metadata of dataset.nc
$ ds meta dataset.nc
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

Select and subset variables. select can also be used to convert between
different file formats (`select <input> <output>`).

Arguments:

- `input` - Input file.
- `output` - Output file.
- `variables` - List of variables (`{ var1 var2 ... }`) or `none` for all.
    Default: `none`.
- `sel` - Selector. Format: `{ <dim1>: <idx1> <dim2>: <idx2> ... }`,
    where `dim<n>` is dimension name and `idx<n>` is a list of indexes
    `{ <i1> <i2> ... }`.

Supported input formats:

- NetCDF4 (`.nc`, `.nc4`, `.nc3`, `.netcdf`, `.hdf`, `.h5`)
- JSON (`.json`)

Supported output formats:

- NetCDF4 (`.nc`, `.nc4`, `.netcdf`)
- JSON (`.json`)

Examples:

```sh
# Write data to dataset.nc
$ ds write dataset.nc { time time { 1 2 3 } } { temperature time { 16. 18. 21. } units: degree_celsius } title: "Temperature data"
# List variables in dataset.nc
$ ds dataset.nc
temperature
time
# Select variable temperature from dataset.nc and write to temperature.nc
$ ds select dataset.nc temperature.nc temperature
# List variables in temperature.nc
$ ds temperature.nc
temperature
# Subset by time index 0 and write to 0.nc
$ ds select dataset.nc 0.nc sel: { time: { 0 } }
# Print variables time and temperature in 0.nc
$ ds cat { time temperature } 0.nc
1,16.0
```

```sh
# Convert dataset.nc to JSON
$ ds select dataset.nc dataset.json
$ cat dataset.json
{"time": [1, 2, 3], "temperature": [16.0, 18.0, 21.0], ".": {"time": {".size": [3], ".dims": ["time"]}, "temperature": {"units": "degree_celsius", ".size": [3], ".dims": ["time"]}, ".": {"title": "Temperature data"}}}
```

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
# Print statistics of variable temperature in dataset.nc
$ ds stats temperature dataset.nc
{
    "count": 3,
    "max": 21.0,
    "mean": 18.333333333333332,
    "median": 18.0,
    "min": 16.0
}
```

#### write

```sh
ds write <output> <var>... <attrs>
```

Write dataset to a file.

Arguments:

- `output` - Output file.
- `var` - Definition of a variable. Format:
    `{ <name> { <dim1> <dim2> } { <x1> <x2> ... } <attrs> }`,
    where `name` is a variable name, `dim<n>` is a dimension name, `x<n>`
    is a value and `<attrs>` are variable-level attributes (key-value pairs).
- `attrs` - Dataset-level attributes (key-value pairs).

Examples:

```python
# Write variables time and temperature to dataset.nc.
ds write dataset.nc { time time { 1 2 3 } } { temperature time { 16. 18. 21. } units: degree_celsius } title: "Temperature data"
```

## Python interface

| Function | Description |
| --- | --- |
| [get_dims](#get_dims) | Get all dimension names in a dataset. |
| [get_vars](#get_vars) | Get all variable names in a dataset. |
| [group_by](#group_by) | Group values along a dimension. |
| [merge](#merge) | Merge datasets along a dimension. |
| [read](#read) | Read dataset from a file. |
| [readdir](#readdir) | Read multiple files in a directory. |
| [rename](#rename) | Rename a variable. |
| [rename_dim](#rename_dim) | Rename a dimension. |
| [select](#select) | Filter dataset by a selector. |
| [write](#write) | Write dataset to a file. |

To import the library:

```python
import ds_format as ds
```

### Constants

#### ds.drivers.netcdf.JD_UNITS

`days since -4713-11-24 12:00 UTC`

NetCDF units for storing Julian date time variables.

#### ds.drivers.netcdf.JD_CALENDAR

`proleptic_greogorian`

NetCDF calendar for storing Julian date time variables.

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

#### group_by

```python
ds.group_by(d, dim, group, func)
```

Group values along a dimension. Each variable with a given dimension `dim`
is split by `group` into subsets. Each subset is replaced with a value computed
by `func`.

Arguments:

- `d` - Dataset (dict).
- `dim` - Dimension to group along (str).
- `group` - Groups (ndarray or list). Array of the same length as the dimension.
- `func` - Group function (function). func(y, axis=i) is called for each subset
`y`, where `i` is the index of the dimension.

Returns None.

#### merge

```python
ds.merge(dd, dim, new=None, variables=None)
```

Merge datasets along a dimension `dim`. If the dimension is not defined in the
dataset, merge along a new dimension `dim`. If `new` is None and `dim` is not
new, variables without the dimension are set with the first occurrence of the
variable. If `new` is not None and `dim` is not new, variables without the
dimension `dim` are merged along a new dimension `new`. If `variables` is not
None, only those variables are merged along a new dimension and other variables
are set to the first occurrence of the variable.

Arguments:

- `dd` - Datasets (list).
- `dim` - Name of a dimension to merge along (str).
- `new` - Name of a new dimension (str) or None.
- `variables` - Variables to merge along a new dimension (list) or None for all
variables.

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

- NetCDF4 (`.nc`, `.nc4`, `.nc3`, `.netcdf`, `.hdf`, `.h5`)
- JSON (`.json`)

Returns dataset (dict).

#### readdir

```python
ds.readdir(dirname, variables=None, merge=None, warnings=[], ...)
```

Read multiple files in a directory.

Arguments:

- `dirname` - Directory name.
- `variables` - Variable names to read (list of str).
- `merge` - Dimension name to merge datasets by.
- `warnings` - Array to be populated with warnings.
- ... - Optional keyword arguments passed to [read](#read).

Returns a list of datasets (list of dict) if `merge` is None or a merged
dataset (dict) if `merge` is a dimension name.

#### rename

```python
ds.rename(d, old, new)
```

Rename a variable. Any dimension with the same name is also renamed.

Arguments:

- `d` - Dataset (dict).
- `old` - Old variable name (str).
- `new` - New variable name (str).

Returns None.

#### rename_dim

```python
ds.rename_dim(d, old, new)
```

Rename a dimension.

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

#### write

```python
ds.write(filename, d)
```

Write dataset to a file. The file type is determined from the file extension.

Arguments:

- `filename` - Filename (str).
- `d` - Dataset (dict).

Supported formats:

- NetCDF4 (`.nc`, `.nc4`, `.netcdf`)
- JSON (`.json`)

Returns None.

## Native format (experimental in 1.2.0-dev)

ds-format implements a native format "ds" (file extension ".ds") in addition to
other standard formats. This format is compatible with the most commonly used
features of NetCDF. Over NetCDF, this format has an advantage of being much
simpler and faster (up to 10 times), especially when reading or writing many
small files. Unlike NetCDF, which is editable, the ds format is inteded to be
written only once (the copy-on-write paradigm). This greatly simplifies the
format and implementation, and improves performance. The ds format can be used
by reading or writing files an extension ".ds". Existing NetCDF files can be
converted to ds with `ds select input.nc output.ds`, where `input.nc` is the
input NetCDF files and `output.ds` is the output ds file.

The format is composed of a header and a body, separated by a newline character
(`\n`). The header is one line containing JSON of the metadata. In addition
to the standard structure described [above](#format-description), the metadata
contains a number of special fields describing where to find and how to decode
the variable data.  The body is a block of binary data directly following the
header. The header and body are separated by a single newline character (`\n`).
The body contains raw bindary data of the variables in a sequential order.

In addition to the variable metadata described [above](#format-description),
the ds native format uses the following properties:

- `.offset`: Data offset in bytes relative to the start of the body.
- `.len`: Length of data in bytes, including a missing data bitmask or string
  lengths, if present.
- `.type`: Data type of the variable. One of:
  `float` (floating-point number) `int` (integer), `uint` (unsigned integer),
  `bool` (boolean), `str` (byte string) and `unicode` (Unicode).
- `.dsize`: Data type size in bits. E.g. if `.type` is `int` and `.dsize` is 64,
  it means the variable data are 64-bit integers.
- `.endian`: Endianness. `b` for big endian, `l` for little endian.
- `.missing`: A boolean value signifying if the data array is a masked array. A
  bitmask of missing data is stored directly after the variable data, and is
  bitpacked.

If missing values are allowed (`.missing` is true), a missing value bitmask is
stored at the variable offset. The bitmask is bitpacked, and at the end it is
padded with zeros to occupy an integer number of bytes. Bit ordering of
bitpacked values is alwyas big endian, regardless of `.endian` of the variable.

The variable data are stored directly after missing value bitmask, or at
variable offset if missing values are not allowed. They are stored as a flat
sequence of binary values in bit ordering as in `.endian`. Multi-dimensional
arrays are stored in the "C ordering" of rows and columns. Missing values are
not written.

Boolean values (type `bool`) are bitpacked, and at the end are padded with
zeros to occupy an integer number of bytes. Bit ordering of bitpacked values is
alwyas big endian, and `.endian` of boolean variables should be `b`.

Data of string arrays (type `str` and `unicode`) are stored as an array of
string lengths, followed by a sequence of the strings, encoded as UTF-8 if the
original strings are Unicode. The array of lengths is a flat array of 64-bit
unsigned integers in bit ordering as in `.endian`. The strings are stored
directly following this array as a sequence of bytes, with no separators between
the strings.

### Performance

The ds format is up 10 times faster than NetCDF, while taking the same or less
space (uncompressed). It is especially faster for reading and writing small
files. Below are results of a set of performance tests which write and read
NetCDF and ds files:

- tiny: one int64 variable of size 1 (`{'x': 1}`).
- small: one int64 variable of size 1000 (`{'x': np.arange(1000)}`).
- large: one float64 variable of size 100x1000x1000 (`{'x': np.ones(100, 1000, 1000)}`).

|                  | time nc (s) | time ds (s) | speed factor | size nc (MB) | size ds (MB) | size factor |
| ---------------- | ----------- | ----------- | ------------ | ------------ | ------------ | ----------- |
| write tiny 100k  | 56          | 11          | 5            | 394          | 394          | 1           |
| write small 100k | 82          | 12          | 7            | 1566         | 785          | 2           |
| write large 10   | 11          | 11          | 1            | 7633         | 7633         | 1           |
| read tiny 100k   | 60          | 6           | 10           |              |              |             |
| read small 100k  | 70          | 8           | 9            |              |              |             |
| read large 10    | 3.3         | 2.5         | 1.3          |              |              |             |

Factors are NetCDF realtive to ds.

## License

This software can be used, shared and  modified freely under the terms of
the MIT license. See [LICENSE.md](LICENSE.md).

## Releases

#### 1.2.0-dev

- New ds file format.

#### 1.1.2 (2022-01-01)

- Fixed handling of NetCDF time variables.
- Fixed merge function definition and implementation.

#### 1.1.1 (2021-12-11)

- Dataset validation on write.
- Dropped support for Python 2.
- merge: new variables option.

#### 1.1.0 (2021-03-31)

- Improved reading of NetCDF time variables.
- Documented readdir function.

#### 1.0.1 (2020-08-12)

- Dependencies installed from PyPI.

#### 1.0.0 (2020-04-28)

- Initial release.
