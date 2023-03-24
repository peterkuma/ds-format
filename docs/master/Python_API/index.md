---
layout: default
title: Python API
---

## Python API

The ds-format Python package provides API for reading, writing and manipulating
data files. The library can be imported with:

```python
import ds_format as ds
```

### Contents

| Function | Description |
| --- | --- |
| [attr](#attr) | Get or set a dataset or variable attribute. |
| [attrs](#attrs) | Get or set variable or dataset attributes. |
| [dim](#dim) | Get a dimension size. |
| [dims](#dims) | Get dataset or variable dimensions or set variable dimensions. |
| [find](#find) | Find a variable, dimension or attribute matching a glob pattern in a dataset. |
| [findall](#findall) | Find variables, dimensions or attributes matching a glob pattern in a dataset. |
| [group_by](#group_by) | Group values along a dimension. |
| [merge](#merge) | Merge datasets along a dimension. |
| [meta](#meta) | Get or set dataset or variable metadata. |
| [read](#read) | Read dataset from a file. |
| [readdir](#readdir) | Read multiple files in a directory. |
| [rename](#rename) | Rename a variable. |
| [rename_attr](#rename_attr) | Rename a dataset or variable attribute. |
| [rename_dim](#rename_dim) | Rename a dimension. |
| [require](#require) | Require that a variable, dimension or attribute is defined in a dataset. |
| [rm](#rm) | Remove a variable. |
| [rm_attr](#rm_attr) | Remove a dataset or variable attribute. |
| [select](#select) | Filter dataset by a selector. |
| [size](#size) | Get variable size. |
| [type](#type) | Get or set variable type. |
| [var](#var) | Get or set variable data. |
| [vars](#vars) | Get all variable names in a dataset. |
| [with_mode](#with_mode) | Context manager which temporarily changes ds.mode. |
| [write](#write) | Write dataset to a file. |

### Constants

#### ds.drivers.netcdf.JD_UNITS

`days since -4713-11-24 12:00 UTC`

NetCDF units for storing Julian date time variables.

#### ds.drivers.netcdf.JD_CALENDAR

`proleptic_greogorian`

NetCDF calendar for storing Julian date time variables.

### Variables

#### mode

Error handling mode. If "strict", handle missing variables, dimensions and
attributes as errors. If "moderate", report a warning. If "soft", ignore
missing items. Overrides the environment variable `DS_MODE`.

Examples:

Set error handling mode to strict.

```
ds.mode = 'strict'
```

### Environment variables

#### DS_MODE

The same as [mode](#mode).

### Functions

{% include_relative functions.md %}
