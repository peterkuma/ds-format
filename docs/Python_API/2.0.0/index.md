---
layout: versioned
version: 2.0.0
title: Python API
---

## Python API

The ds-format Python package provides API for reading, writing and manipulating
data fies. The library can be imported with:

```python
import ds_format as ds
```

### Contents

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

