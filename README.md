# ds_format

**Development status:** in development

ds_format is a Python implementation of a dataset
format DS for storing data along with metadata, similar to
[NetCDF](https://www.unidata.ucar.edu/software/netcdf/)
and [HDF](https://www.hdfgroup.org).
DS is based on JSON-like data types commonly available in high-level
programming
languages. The API is designed so that functions are completely separated
from data (unlike in object oriented programming) and data has the same
representation in memory as on disk. DS is a subset of NetCDF, and can be
stored in this format, which is also the recommended
on-disk format. Operators are provided for manipulating datasets.

## Dataset format description

The general structure of a dataset is:

```
d = {
	"variable-1": [...],
	"variable-2": [...],
	...,
	".": {
		"variable-1": {
			".dims": ["dimension-1", "dimension-2", ...],
			"attribute-1": ...,
			"attribute-2": ...,
			...
		},
		"variable-2": {
			".dims": ["dimension-1", "dimension-2", ...],
			"attribute-1": ...,
			"attribute-2": ...,
			...
		},
		...
		".": {
			"attribute-1": ...,
			"attribute-2": ...,
			...
		}
	}
}
```

where `d['variable-...']` are variables containing multi-dimensional (NumPy)
arrays, and `d['.']` stores the metadata. `d['.']['variable-...']` contain
metadata of each variable: dimension list `d['variable-...']['.dims']` and an
arbitrary number of variable-level attributes. `d['.']['.']` contains an
arbitrary number dataset-level attributes.

## Installation

Requirements:

- Python 2.7 or Python 3

To install in system directories:

```sh
python setup.py install
```

To install in user directories (make sure `~/.local/bin/` is in the `PATH`
environment variable):

```sh
python setup.py install --user
```

## Python interface

### I/O

#### read(filename, [vars])

Read dataset from a file, optionally reading only specified variables.

- `filename` - file name (str)
- `vars` - variable names to read (list of str)

Returns dataset (dict).

#### to_netcdf(filename, d)

Write dataset to a NetCDF file.

- `filename` - file name (str)
- `d` - dataset (dict)

### Operators

#### filter(d, sel)

Filter dataset by a selector.

- `d` - dataset (dict)
- `sel` - selector (dict)

Selector is a dictionary where each key is a dimension name and value
is a mask to apply along the dimension.

Returns nothing.

#### get_dims(d)

Get dataset dimension names.

- `d` - dataset (dict)

Returns dimension names (list of str).

#### get_vars(d)

Get dataset variable names.

- `d` - dataset (dict)

Returns variable names (list of str).

#### merge(dd, dim)

Merge datasets along a dimension. Variables with incompatible dimensions
will contain the first value encountered.

- `dd` - datasets (list of dict)
- `dim` - name of dimension (str)

Returns a dataset (dict).

## Command line interface

### Synopsis

    ds [<cmd>] [<options>...]

### Commands

#### ls

   ds ls [-l] <input>...

- **-l** - print a detailed list

List variables.

#### cat

    ds cat <var>[,<var>]... <input>

Print variable content.

#### stats

    ds stats <var> <input>

Print variable statistics.

#### merge

    ds merge <dim> <input>... <output>

Merge input files along a dimension.

#### get

    ds get <path> <input>

Get attribute at path.
