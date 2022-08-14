{% raw %}#### attrs

Print attributes in a dataset.

Usage: `ds attrs` [*var*] *input*

The output is formatted as [PST](https://github.com/peterkuma/pst).

Arguments:

- *var*: Variable name.
- *input*: Input file.

Examples:

Print dataset attributes in `dataset.nc`.

```
$ ds attrs dataset.nc
title: "Temperature data"
```

Print attributes of the variable `temperature` in `dataset.nc`.

```
$ ds attrs temperature dataset.nc
long_name: temperature units: celsius
```

#### cat

Print variable.

Usage: 

`ds cat` [*options*] *var* *input*<br />
`ds cat` [*options*] *var*... *input*<br />


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
16.000000
18.000000
21.000000
```

Print time and temperature values in dataset.nc.

```
$ ds cat time temperature dataset.nc
1 16.000000
2 18.000000
3 21.000000
```

#### dims

Print dimensions of a dataset or a variable.

Usage: `ds dims` [*var*] *input*

Arguments:

- *var*: Variable to print dimensions of.
- *input*: Input file.

Options:

- `-s`, `--size`: If *var* is defined, print the size of dimensions as an object instead of an array of dimensions. The order is not guaranteed.

Examples:

Print dimensions of a dataset.

```
$ ds dims dataset.nc
time
```

Print dimensions of the variable `temperature`.

```
$ ds dims temperature dataset.nc
time
```

#### get

Get attribute at path.

Usage: `ds get` *path* *input*

Arguments:

- *path*: Attribute path.
- *input*: Input file.

#### ls

List variables.

Usage: 

`ds` [*options*] [*var*]... *input*<br />
`ds ls` [*options*] [*var*]... *input*<br />


Lines in the output are formatted as [PST](https://github.com/peterkuma/pst).

Arguments:

- *var*: Variable name to list.
- *input*: Input file.

Options:

- `-l`: Print a detailed list of variabes (name and dimensions), preceded with a line with dataset dimensions.
- `a:` *attrs*: Print variable attributes. *attrs* can be a string or an array.

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
time: 3
temperature
time
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

Merge datasets along a dimension.

Usage: `ds merge` *dim* *input*... *output* [*options*]

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

Print dataset metadata.

Usage: `ds meta` [*var*] [*input*]

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

#### rename

Rename variables and attributes.

Usage: 

`ds rename` *vars* *input* *output*<br />
`ds rename` *var* *attrs* *input* *output*<br />
`ds rename` `{` *var* *attrs* `}`... *input* *output*<br />


Arguments:

- *var*: Variable name or an array of variable names whose attributes to rename or `none` to change dataset attributes.
- *vars*: Pairs of old and new variable names as *var*`:` *newvar*. If *newattr* is `none`, remove the attribute.
- *attrs*: Pairs of old and new attribute names as *attr*`:` *newattr*. If *newattr* is `none`, remove the attribute.
- *input*: Input file.
- *output*: Output file.

Examples:

Rename variable `time` to `newtime` and `temperature` to `newtemperature` in `dataset.nc` and save the output in `output.nc`.

```
$ ds rename time: newtime temperature: newtemperature dataset.nc output.nc
```

Rename a dataset attribute `title` to `newtitle` in `dataset.nc` and save the output in `output.nc`.

```
$ ds rename none title: newtitle dataset.nc output.nc
```

Rename an attribute `units` of a variable `temperature` to `newunits` in `dataset.nc` and save the output in `output.nc`.

```
$ ds rename temperature units: newunits dataset.nc output.nc
```

#### rename_dim

Rename a dimension.

Usage: 

`ds rename_dim` *old* *new* *input* *output*<br />
`ds rename_dim` { *old* *new* }... *input* *output*<br />


Arguments:

- *old*: Old dimension name.
- *new*: New dimension name.
- *input*: Input file.
- *output*: Output file.

Examples:

Rename dimension `time` to `newtime` in `dataset.nc` and save the output in `output.nc`.

```
$ ds -l dataset.nc
time: 3
temperature
time
$ ds rename_dim time newtime dataset.nc output.nc
$ ds -l output.nc
newtime: 3
temperature
time
```

#### rm

Remove variables or attributes.

Usage: 

`ds rm` *var* *input* *output*<br />
`ds rm` *var* *attr* *input* *output*<br />


Arguments:

- *var*: Variable name, an array of variable names or `none` to remove a dataset attribute.
- *attr*: Attribute name or an array of attribute names.
- *input*: Input file.
- *output*: Output file.

Examples:

Remove a variable `temperature` from `dataset.nc` and save the output in `output.nc`.

```
$ ds rm temperature dataset.nc output.nc
```

Remove variables `time` and `temperature` from `dataset.nc` and save the output in `output.nc`.

```
$ ds rm { time temperature } dataset.nc output.nc
```

Remove an attribute `title` from `dataset.nc` and save the output in `output.nc`.

```
$ ds rm none title dataset.nc output.nc
```

Remove an attribute `units` of the variable `temperature` in `dataset.nc` and save the output in `output.nc`.

```
$ ds rm temperature title dataset.nc output.nc
```

#### select

Select and subset variables.

Usage: `ds select` *input* *output* [*variables*] [*options*]

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

#### set

Set variable data, dimensions and attributes in a dataset.

Usage: 

`ds set` *ds_attrs* *input* *output*<br />
`ds set` *var* *dims* [*data*] [*attrs*]... *input* *output*<br />
`ds set` `{` *var* *dims* [*data*] [*attrs*]... `}`... *ds_attrs* *input* *output*<br />


Arguments:

- *var*: Variable name or `none` to set dataset attributes.
- *dims*: Variable dimension name (if single), an array of variable dimensions (if multiple), `none` to keep original dimension or autogenerate if a new variable, or `{ }` to autogenerate new dimension names.
- *data*: Variable data. This can be a [PST](https://github.com/peterkuma/pst)-formatted scalar or an array.
- *attrs*: Variable attributes or dataset attributes if *var* is `none` as *attr*: *value* pairs.
- *ds_attrs*: Dataset attributes as *attr*: *value* pairs.
- *input*: Input file or `none` for a new file to be created.
- *output*: Output file.

Examples:

Write variables `time` and `temperature` to `dataset.nc`.

```
$ ds set { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: "Temperature data" none dataset.nc
```

Set data of a variable `temperature` to an array of 16.0, 18.0, 21.0 in `dataset.nc` and save the output in `output.nc`.

```
$ ds set temperature { 16. 18. 21. } dataset.nc output.nc
```

Set a dimension of a  variable `temperature` to time, data to an array of 16.0, 18.0, 21.0, its attributes `long_name` to "temperature" and `units` to "celsius" in `dataset.nc` and save the output in `output.nc`.

```
$ ds set temperature time { 16. 18. 21. } long_name: temperature units: celsius dataset.nc output.nc
```

Set multiple variables in `dataset.nc` and save the output in `output.nc`.

```
$ ds set { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: "Temperature data" dataset.nc output.nc
```

Set an attribute `newtitle` to `New title` in `dataset.nc` and save the output in `output.nc`.

```
$ ds set newtitle: "New title" dataset.nc output.nc
```

Set an attribute `newunits` of a variable `temperature` to `K` in `dataset.nc` and save the output in `output.nc`.

```
$ ds set temperature newunits: K dataset.nc output.nc
```

#### stats

Print variable statistics.

Usage: `ds stats` *var* *input*

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

{% endraw %}