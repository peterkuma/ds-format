# ds_format

**Development status:** in development

ds_format is a Python implementation of a dataset
format *DS* for storing data along with metadata, similar to
[NetCDF](https://www.unidata.ucar.edu/software/netcdf/)
and [HDF](https://www.hdfgroup.org).
DS is based on [JSON](https://json.org/)-like data structures commonly
available in high-level
programming languages. The API is designed so that functions are completely
separated
from data (unlike in object oriented programming), and data has the same
representation in the memory as on the disk. DS supports a subset
of functionality of NetCDF,
and can be stored in this format, which is also the recommended
on disk format. The Python library **ds_format** implements I/O and operators
for manipulation of datasets, and the command line program **ds** implements
access to DS files.

## DS format description

The general structure of the DS format is:

```python
d = {
    "<var-1>": [...],
    "<var-2>": [...],
    ...,
    ".": {
        "<var-1>": {
            ".dims": ["<dim-1>", "<dim-2>", ...],
            "<attr-1>": ...,
            "<attr-2>": ...,
            ...
        },
        "<var-2>": {
            ".dims": ["<dim-1>", "<dim-2>", ...],
            "<attr-1>": ...,
            "<attr-2>": ...,
            ...
        },
        ...
        ".": {
            "<attr-1>": ...,
            "<attr-2>": ...,
            ...
        }
    }
}
```

where `d['<var-...>']` are variables containing multi-dimensional
[NumPy](https://www.numpy.org/)
arrays, and `d['.']` stores the metadata. `d['.']['<var-...>']` contain
metadata of each variable: dimension list `.dims` and an
arbitrary number of variable-level attributes. `d['.']['.']` contains an
arbitrary number of dataset-level attributes.

## Installation

Requirements:

- [Python 2.7](https://www.python.org/), or a Python 2.7 distribution such
as [Anaconda](https://www.anaconda.com/distribution/)
- [netCDF4](http://unidata.github.io/netcdf4-python/netCDF4/index.html)
- [Aquarius Time](https://github.com/peterkuma/aquarius-time)

To install:

```sh
pip install [--user] https://github.com/peterkuma/aquarius-time/archive/master.zip
python setup.py install [--user]
```

## Python interface

To import the library:

```python
import ds_format as ds
```

### I/O

#### ds.read(filename, [vars], full=False, jd=False)

Read dataset from a file, optionally reading only specified variables.

- `filename` – file name (str)
- `vars` – variable names to read (list of str)
- `full` – read all metadata
- `jd` – convert time variables to Julian dates (JD)
(see [Aquarius Time](https://github.com/peterkuma/aquarius-time))

Supported formats:

- NetCDF4 (`.nc`)

Returns dataset (dict).

#### ds.to_netcdf(filename, d)

Write dataset to a NetCDF file.

- `filename` – file name (str)
- `d` – dataset (dict)

Returns None.

### Operators

#### ds.filter(d, sel)

Filter dataset by a selector.

- `d` – dataset (dict)
- `sel` – selector (dict)

Selector is a dictionary where each key is a dimension name and value
is a mask to apply along the dimension.

Returns None.

#### ds.get_dims(d)

Get dataset dimension names.

- `d` – dataset (dict)

Returns dimension names (list of str).

#### ds.get_vars(d)

Get dataset variable names.

- `d` – dataset (dict)

Returns variable names (list of str).

#### ds.merge(dd, dim, new=False)

Merge datasets along a dimension. Variables with incompatible dimensions
will contain the first value encountered.

- `dd` – datasets (list of dict)
- `dim` – name of dimension (str)
- `new` – merge datasets along a new dimension (str)

Returns a dataset (dict).

#### ds.rename(d, old, new)

Rename variable `old` to `new`.

- `d` – dataset (dict)
- `old` – old variable name
- `new` – new variable name

Returns None.

## Command line interface

### Synopsis

```sh
ds [<cmd>] [<options>...]
```

### Commands

#### *default*

```sh
ds <input>
```

Print metadata.

#### ls

```sh
ds ls [-l] <input>...
```

- **-l** – print a detailed list

List variables.

#### cat

```sh
ds cat <var>[,<var>]... <input>
```

Print variable content.

#### stats

```sh
ds stats <var> <input>
```

Print variable statistics.

#### merge

```sh
ds merge <dim> <input>... <output>
```

Merge input files along a dimension.

#### get

```sh
ds get <path> <input>
```

Get attribute at path.

## License

This software is published under the terms of the MIT license
(see [LICENSE.md](LICENSE.md)).
