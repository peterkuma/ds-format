---
layout: default
title: Command line
---

## Command line

The ds-format Python package provides a command `ds` for reading, writing
and manipulating data files.

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
