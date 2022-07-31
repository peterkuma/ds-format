{% raw %}#### cat

Print variable.

Usage:

`ds cat` [*options*] *var* *input*<br />
`ds cat` [*options*] `{` *var*... `}` *input*<br />


Arguments:

- *var*: Variable name.
- *input*: Input file.

Options:

- `-h`: Print human-readable values.
- `--jd`: Convert time variables to Julian dates (see [Aquarius Time](https://github.com/peterkuma/aquarius-time)).

Examples:

Print temperature values in dataset.nc.

```
$ ds cat temperature dataset.nc
16.0
18.0
21.0
```

Print time and temperature values in dataset.nc.

```
$ ds cat { time temperature } dataset.nc
1,16.0
2,18.0
3,21.0
4,23.0
5,25.0
6,28.0
```

#### get

Get attribute at path.

Usage:`ds get` *path* *input*

Arguments:

- *path*: Attribute path.
- *input*: Input file.

#### ls

List variables.

Usage:

`ds` [*options*] *input*...<br />
`ds ls` [*options*] *input*...<br />


Lines in the output are formatted as [PST](https://github.com/peterkuma/pst).

Arguments:

- *input*: Input file.

Options:

- `-l`: Print a detailed list (name and dimensions).
- `-a` *attrs*: Print given variable attributes. *attrs* can be a string or an array.

Examples:

Print a list of variables in dataset.nc.

```
$ ds dataset.nc
temperature
time
```

Print a detailed list of variables in dataset.nc.

```
$ ds -l dataset.nc
temperature time: 3
time time: 3
```

Print a list of variables with an attribute `units`.

```
$ ds dataset.nc a: units
temperature celsius
time s
```

Print a list of variables with attributes `long_name` and `units`.

```
$ ds dataset.nc a: { long_name units }
temperature temperature celsius
time time s
```

#### merge

Merge datasets along a dimension dim.

Usage:`ds merge` *dim* *input*... *output* [*options*]

Merge datasets along a dimension *dim*. If the dimension is not defined in the dataset, merge along a new dimension *dim*. If *new* is `none` and *dim* is not new, variables without the dimension are set with the first occurrence of the variable. If *new* is not `none` and *dim* is not new, variables without the dimension dim are merged along a new dimension *new*. If variables is not `none`, only those variables are merged along a new dimension and other variables are set to the first occurrence of the variable.

Arguments:

- *dim*: Name of a dimension to merge along.
- *input*: Input file.
- *output*: Output file.

Options:

- `new:` *value*: Name of a new dimension.
- `variables:` `{` *value*... `}`: Variables to merge along a new dimension or none for all variables.

Examples:

Write example data to dataset1.nc.

```
$ ds write dataset1.nc { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: "Temperature data"
```

Write example data to dataset2.nc.

```
$ ds write dataset2.nc { time time { 4 5 6 } long_name: time units: s } { temperature time { 23. 25. 28. } long_name: temperature units: celsius title: "Temperature data"
```

Merge dataset1.nc and dataset2.nc and write the result to dataset.nc.

```
$ ds merge time dataset1.nc dataset2.nc dataset.nc
```

Print time and temperature variables in dataset.nc.

```
$ ds cat { time temperature } dataset.nc
1,16.0
2,18.0
3,21.0
4,23.0
5,25.0
6,28.0
```

#### meta

Print metadata.

Usage:`ds meta` [*var*] [*input*]

The output is formatted as [PST](https://github.com/peterkuma/pst).

Arguments:

- *input*: Input file.
- *var*: Variable name to print metadata for. If not specified, print metadata for the whole file.

Examples:

Print metadata of dataset.nc.

```
$ ds meta dataset.nc
.: {{
	title: "Temperature data"
}}
time: {{
	long_name: time
	units: s
	.dims: { time }
	.size: { 3 }
}}
temperature: {{
	long_name: temperature
	units: celsius
	.dims: { time }
	.size: { 3 }
}}
```

#### select

Select and subset variables.

Usage:`ds select` *input* *output* [*variables*] [*options*]

select can also be used to convert between different file formats (`ds select` *input* *output*).

Arguments:

- *input*: Input file.
- *output*: Output file.
- *variables*: List of variables as `{` *var1* *var2* ... `}` or `none` for all. Default: `none`.

Options:

- `sel:` `{` *dim1*: *idx1* *dim2*: *idx2* ... `}`: Selector, where *dim* is dimension name and *idx* is a list of indexes as `{` *i1* *i2* ... `}`.

Supported input formats:

- NetCDF4: `.nc`, `.nc4`, `.nc3`, `.netcdf`, `.hdf`, `.h5`
- JSON: `.json`

Supported output formats:

- NetCDF4: `.nc`, `.nc4`, `.netcdf`
- JSON: `.json`

Examples:

Write data to dataset.nc.

```
$ ds write dataset.nc { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius title: "Temperature data"
```

List variables in dataset.nc.

```
$ ds dataset.nc
temperature
time
```

Select variable temperature from dataset.nc and write to temperature.nc.

```
$ ds select dataset.nc temperature.nc temperature
```

List variables in temperature.nc.

```
$ ds temperature.nc
temperature
```

Subset by time index 0 and write to 0.nc.

```
$ ds select dataset.nc 0.nc sel: { time: { 0 } }
```

Print variables time and temperature in 0.nc.

```
$ ds cat { time temperature } 0.nc
1,16.0
```

Convert dataset.nc to JSON.

```
$ ds select dataset.nc dataset.json
$ cat dataset.json
{"time": [1, 2, 3], "temperature": [16.0, 18.0, 21.0], ".": {".": {"title": "Temperature data"}, "time": {"long_name": "time", "units": "s", ".dims": ["time"], ".size": [3]}, "temperature": {"long_name": "temperature", "units": "celsius ".dims": ["time"], ".size": [3]}}}
```

#### stats

Print variable statistics.

Usage:`ds stats` *var* *input*

The output is formatted as [PST](https://github.com/peterkuma/pst).

Arguments:

- *var*: Variable name.
- *input*: Input file.

Output description:

- `count`: Number of array elements.
- `max`: Maximum value.
- `mean`: Sample mean.
- `median`: Sample median.
- `min`: Minimum value.

Examples:

Print statistics of variable temperature in dataset.nc.

```
$ ds stats temperature dataset.nc
count: 3 min: 16.000000 max: 21.000000 mean: 18.333333 median: 18.000000
```

#### write

Write dataset to a file.

Usage:`ds write` *output* *var* ... *attrs*

Arguments:

- *output*: Output file.
- *var*: Definition of a variable as `{` *name* `{` *dim* ... `}` `{` *x* ... `}` *attrs* `}`, where *name* is a variable name, *dim* is a dimension name, *x* is a value and *attrs* are variable-level attributes (key-value pairs).
- *attrs*: Dataset-level attributes (key-value pairs).

Examples:

Write variables time and temperature to dataset.nc.

```
ds write dataset.nc { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: "Temperature data"
```

{% endraw %}