---
layout: versioned
version: master
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
| [attr](#attr) | Get or set a dataset or variable attribute. |
| [attrs](#attrs) | Get variable or dataset attributes. |
| [dim](#dim) | Get a dimension size. |
| [dims](#dims) | Get dataset or variable dimensions or set variable dimensions. |
| [group_by](#group_by) | Group values along a dimension. |
| [merge](#merge) | Merge datasets along a dimension. |
| [meta](#meta) | Get dataset or variable metadata. |
| [read](#read) | Read dataset from a file. |
| [readdir](#readdir) | Read multiple files in a directory. |
| [rename](#rename) | Rename a variable. |
| [rename_attr](#rename_attr) | Rename a dataset or variable attribute. |
| [rename_dim](#rename_dim) | Rename a dimension. |
| [rm](#rm) | Remove a variable. |
| [rm_attr](#rm_attr) | Remove a dataset or variable attribute. |
| [select](#select) | Filter dataset by a selector. |
| [var](#var) | Get or set variable data. |
| [vars](#vars) | Get all variable names in a dataset. |
| [write](#write) | Write dataset to a file. |

<!--| [find](#find) | Find a variable, dimension or attribute matching a pattern. |-->
<!--| [findall](#findall) | Find variables, dimensions or attributes matching a pattern. |-->
<!--| [require](#require) | Require a variable, dimension or attribute to be present in a dataset. |-->

### Constants

#### ds.drivers.netcdf.JD_UNITS

`days since -4713-11-24 12:00 UTC`

NetCDF units for storing Julian date time variables.

#### ds.drivers.netcdf.JD_CALENDAR

`proleptic_greogorian`

NetCDF calendar for storing Julian date time variables.

### Functions

{% include functions.md %}
