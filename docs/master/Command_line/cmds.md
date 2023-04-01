{% raw %}#### attrs

Print attributes in a dataset.

**Usage:** `ds attrs` [*var*] [*attr*] *input* [*options*]

The output is formatted as [PST](https://github.com/peterkuma/pst).

**Arguments:**

- *var*: Variable name or `none` to print a dataset attribute *attr*. If omitted, print all dataset attributes.
- *attr*: Attribute name.
- *input*: Input file.
- *options*: See help for ds for global options.

**Examples:**

Print dataset attributes in `dataset.nc`.

```
$ ds attrs dataset.nc
title: "Temperature data"
```

Print attributes of a variable `temperature` in `dataset.nc`.

```
$ ds attrs temperature dataset.nc
long_name: temperature units: celsius
```

Print a dataset attribute `title`.

```
$ ds attrs none title dataset.nc
"Temperature data"
```

Print an attribute units of a variable `temperature`.

```
$ ds attrs temperature units dataset.nc
celsius
```

#### cat

Print variable data.

**Usage:** 

`ds cat` *var* *input* [*options*]<br />
`ds cat` *var*... *input* [*options*]<br />


Data are printed by the first index, one item per line, formatted as [PST](https://github.com/peterkuma/pst)-formatted. If multiple variables are selected, items at a given index from all variables are printed on the same line as an array. The first line is a header containing a list of variables. Missing values are printed as empty rows (if printing one single dimensional variable) or as `none`.

**Arguments:**

- *var*: Variable name.
- *input*: Input file.
- *options*: See help for ds for global options.

**Options:**

- `-h`: Print human-readable values (time as ISO 8601).
- `--jd`: Convert time variables to Julian date (see [Aquarius Time](https://github.com/peterkuma/aquarius-time)).

**Examples:**

Print temperature values in dataset.nc.

```
$ ds cat temperature dataset.nc
temperature
16.000000
18.000000
21.000000
```

Print time and temperature values in dataset.nc.

```
$ ds cat time temperature dataset.nc
time temperature
1 16.000000
2 18.000000
3 21.000000
```

#### dims

Print dimensions of a dataset or a variable.

**Usage:** `ds dims` [*var*] *input* [*options*]

**Arguments:**

- *var*: Variable to print dimensions of.
- *input*: Input file.
- *options*: See help for ds for global options.

**Options:**

- `-s`, `--size`: If *var* is defined, print the size of dimensions as an object instead of an array of dimensions. The order is not guaranteed.

**Examples:**

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

#### ls

List variables.

**Usage:** 

`ds` [*var*]... *input* [*options*]<br />
`ds ls` [*var*]... *input* [*options*]<br />


Lines in the output are formatted as [PST](https://github.com/peterkuma/pst).

**Arguments:**

- *var*: Variable name to list.
- *input*: Input file.
- *options*: See help for ds for global options.

**Options:**

- `-l`: Print a detailed list of variables (name, type and an array of dimensions), preceded with a line with dataset dimensions.
- `a:` *attrs*: Print variable attributes after the variable name and dimensions. *attrs* can be a string or an array.

**Examples:**

Print a list of variables in `dataset.nc`.

```
$ ds ls dataset.nc
temperature
time
```

Print a detailed list of variables in `dataset.nc`.

```
$ ds ls -l dataset.nc
time: 3
temperature float64 { time }
time int64 { time }
```

Print a list of variables with an attribute `units`.

```
$ ds ls dataset.nc a: units
temperature celsius
time s
```

Print a list of variables with attributes `long_name` and `units`.

```
$ ds ls dataset.nc a: { long_name units }
temperature temperature celsius
time time s
```

Print all variables matching a glob "temp*" in `dataset.nc`.

```
$ ds ls 'temp*' dataset.nc
temperature
```

#### merge

Merge datasets along a dimension.

**Usage:** `ds merge` *dim* *input*... *output* [*options*]

Merge datasets along a dimension *dim*. If the dimension is not defined in the dataset, merge along a new dimension *dim*. If *new* is `none` and *dim* is not new, variables without the dimension *dim* are set with the first occurrence of the variable. If *new* is not `none` and *dim* is not new, variables without the dimension *dim* are merged along a new dimension *new*. If *variables* is not `none`, only those variables are merged along a new dimension, and other variables are set to the first occurrence of the variable. Variables which are merged along a new dimension and are not present in all datasets have their subsets corresponding to the datasets where they are missing filled with missing values. Dataset and variable metadata are merged sequentially from all datasets, with metadata from later datasets overriding metadata from the former ones.

**Arguments:**

- *dim*: Name of a dimension to merge along.
- *input*: Input file.
- *output*: Output file.
- *options*: See help for ds for global options.

**Options:**

- `new:` *value*: Name of a new dimension or `none`.
- `variables:` `{` *value*... `}` \| `none`: Variables to merge along a new dimension or `none` for all variables.
- `jd:` *value*: If `true`, convert time to Julian date when merging time variables with unequal units. If `false`, merge time variables as is. Default: `true`.

**Examples:**

Write example data to dataset1.nc.

```
$ ds set { time none time { 1 2 3 } long_name: time units: s } { temperature none time { 16. 18. 21. } long_name: temperature units: celsius } title: "Temperature data" none dataset1.nc
```

Write example data to dataset2.nc.

```
$ ds set { time none time { 4 5 6 } long_name: time units: s } { temperature none time { 23. 25. 28. } long_name: temperature units: celsius } title: "Temperature data" none dataset2.nc
```

Merge dataset1.nc and dataset2.nc and write the result to dataset.nc.

```
$ ds merge time dataset1.nc dataset2.nc dataset.nc
```

Print time and temperature variables in dataset.nc.

```
$ ds cat time temperature dataset.nc
time temperature
1 16.000000
2 18.000000
3 21.000000
4 23.000000
5 25.000000
6 28.000000
```

#### meta

Print dataset metadata.

**Usage:** `ds meta` [*var*] *input* [*options*]

The output is formatted as [PST](https://github.com/peterkuma/pst).

**Arguments:**

- *input*: Input file.
- *var*: Variable name to print metadata for or "." to print dataset metadata. If not specified, print metadata for the whole file.
- *options*: See help for ds for global options.

**Examples:**

Print metadata of `dataset.nc`.

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

**Usage:** 

`ds rename` *vars* *input* *output* [*options*]<br />
`ds rename` *var* *attrs* *input* *output* [*options*]<br />
`ds rename` `{` *var* *attrs* `}`... *input* *output* [*options*]<br />


**Arguments:**

- *var*: Variable name, or an array of variable names whose attributes to rename, or `none` to rename dataset attributes.
- *vars*: Pairs of old and new variable names as *oldvar*`:` *newvar*. If *newattr* is `none`, remove the attribute.
- *attrs*: Pairs of old and new attribute names as *oldattr*`:` *newattr*. If *newattr* is `none`, remove the attribute.
- *input*: Input file.
- *output*: Output file.
- *options*: See help for ds for global options. Note that with this command *options* can only be supplied before the command name or at the end of the command line.

**Examples:**

Rename variables `time` to `newtime` and `temperature` to `newtemperature` in `dataset.nc` and save the output in `output.nc`.

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

**Usage:** 

`ds rename_dim` *dims* *input* *output* [*options*]<br />


**Arguments:**

- *dims*: Pairs of old and new dimension names as *olddim*`:` *newdim*.
- *input*: Input file.
- *output*: Output file.
- *options*: See help for ds for global options. Note that with this command *options* can only be supplied before the command name or at the end of the command line.

**Examples:**

Rename dimension `time` to `newtime` in `dataset.nc` and save the output in `output.nc`.

```
$ ds -l dataset.nc
time: 3
temperature
time
$ ds rename_dim time: newtime dataset.nc output.nc
$ ds -l output.nc
newtime: 3
temperature
time
```

#### rm

Remove variables or attributes.

**Usage:** 

`ds rm` *var* *input* *output* [*options*]<br />
`ds rm` *var* *attr* *input* *output* [*options*]<br />


**Arguments:**

- *var*: Variable name, an array of variable names or `none` to remove a dataset attribute.
- *attr*: Attribute name or an array of attribute names.
- *input*: Input file.
- *output*: Output file.
- *options*: See help for ds for global options.

**Examples:**

Remove a variable `temperature` in `dataset.nc` and save the output in `output.nc`.

```
$ ds rm temperature dataset.nc output.nc
```

Remove variables `time` and `temperature` in `dataset.nc` and save the output in `output.nc`.

```
$ ds rm { time temperature } dataset.nc output.nc
```

Remove a dataset attribute `title` in `dataset.nc` and save the output in `output.nc`.

```
$ ds rm none title dataset.nc output.nc
```

Remove an attribute `units` of a variable `temperature` in `dataset.nc` and save the output in `output.nc`.

```
$ ds rm temperature units dataset.nc output.nc
```

#### select

Select and subset variables.

**Usage:** `ds select` [*var*...] [*sel*] *input* *output* [*options*]

select can also be used to convert between different file formats (`ds select` *input* *output*).

**Arguments:**

- *var*: Variable name.
- *sel*: Selector as *dim*`:` *idx* pairs, where *dim* is a dimension name and *idx* is an index or a list of indexes as `{` *i*... `}`.
- *input*: Input file.
- *output*: Output file.
- *options*: See help for ds for global options. Note that with this command *options* can only be supplied before the command name or at the end of the command line.

**Examples:**

Write data to dataset.nc.

```
$ ds set { time none time { 1 2 3 } long_name: time units: s } { temperature none time { 16. 18. 21. } long_name: temperature units: celsius } title: "Temperature data" none dataset.nc
```

List variables in dataset.nc.

```
$ ds dataset.nc
temperature
time
```

Select variable temperature from dataset.nc and write to temperature.nc.

```
$ ds select temperature dataset.nc temperature.nc
```

List variables in temperature.nc.

```
$ ds temperature.nc
temperature
```

Subset by time index 0 and write to 0.nc.

```
$ ds select time: 0 dataset.nc 0.nc
```

Print variables time and temperature in 0.nc.

```
$ ds cat time temperature 0.nc
time temperature
1 16.000000
```

Convert dataset.nc to JSON.

```
$ ds select dataset.nc dataset.json
$ cat dataset.json
{"time": [1, 2, 3], "temperature": [16.0, 18.0, 21.0], ".": {".": {"title": "Temperature data"}, "time": {"long_name": "time", "units": "s", ".dims": ["time"], ".size": [3]}, "temperature": {"long_name": "temperature", "units": "celsius ".dims": ["time"], ".size": [3]}}}
```

#### set

Set variable data, dimensions and attributes in an existing or new dataset.

**Usage:** 

`ds set` *ds_attrs* *input* *output* [*options*]<br />
`ds set` *var* [*type* [*dims* [*data*]]] [*attrs*]... *input* *output* [*options*]<br />
`ds set` `{` *var* [*type* [*dims* [*data*]]] [*attrs*]... `}`... *ds_attrs* *input* *output* [*options*]<br />


**Arguments:**

- *var*: Variable name.
- *type*: Variable type (`str`), or `none` to keep the original type if *data* is not supplied or autodetect based on *data* if *data* is supplied. One of: `float32` and `float64` (32-bit and 64-bit floating-point number, resp.), `int8`, `int16`, `int32` and `int64` (8-bit, 16-bit, 32-bit and 64-bit integer, resp.), `uint8`, `uint16`, `uint32` and `uint64` (8-bit, 16-bit, 32-bit and 64-bit unsigned integer, resp.), `bool` (boolean), `str` (string) and `unicode` (Unicode).
- *dims*: Variable dimension name (if single), an array of variable dimensions (if multiple), `none` to keep original dimension or autogenerate if a new variable, or `{ }` to autogenerate new dimension names.
- *data*: Variable data. This can be a [PST](https://github.com/peterkuma/pst)-formatted scalar or an array. `none` values are interpreted as missing values.
- *attrs*: Variable attributes or dataset attributes if *var* is `none` as *attr*`:` *value* pairs.
- *ds_attrs*: Dataset attributes as *attr*`:` *value* pairs.
- *input*: Input file or `none` for a new file to be created.
- *output*: Output file.
- *options*: See help for ds for global options. Note that with this command *options* can only be supplied before the command name or at the end of the command line.

**Examples:**

Write variables `time` and `temperature` to `dataset.nc`.

```
$ ds set { time none time { 1 2 3 } long_name: time units: s } { temperature none time { 16. 18. 21. } long_name: temperature units: celsius } title: "Temperature data" none dataset.nc
```

Set data of a variable `temperature` to an array of 16.0, 18.0, 21.0 in `dataset.nc` and save the output in `output.nc`.

```
$ ds set temperature none none { 16. 18. 21. } dataset.nc output.nc
```

Set a dimension of a  variable `temperature` to time, data to an array of 16.0, 18.0, 21.0, its attribute `long_name` to "temperature" and `units` to "celsius" in `dataset.nc` and save the output in `output.nc`.

```
$ ds set temperature none time { 16. 18. 21. } long_name: temperature units: celsius dataset.nc output.nc
```

Set multiple variables in `dataset.nc` and save the output in `output.nc`.

```
$ ds set { time none time { 1 2 3 } long_name: time units: s } { temperature none time { 16. 18. 21. } long_name: temperature units: celsius } title: "Temperature data" dataset.nc output.nc
```

Set a dataset attribute `newtitle` to `New title` in `dataset.nc` and save the output in `output.nc`.

```
$ ds set newtitle: "New title" dataset.nc output.nc
```

Set an attribute `newunits` of a variable `temperature` to `K` in `dataset.nc` and save the output in `output.nc`.

```
$ ds set temperature newunits: K dataset.nc output.nc
```

#### size

Print a variable size.

**Usage:** `ds size` *var* *input* [*options*]

**Arguments:**

- *var*: Variable to print the size of.
- *input*: Input file.
- *options*: See help for ds for global options.

**Examples:**

Print the size of a variable `temperature` in a dataset `dataset.nc`.

```
$ ds size temperature dataset.nc
3
```

#### stats

Print variable statistics.

**Usage:** `ds stats` *var* *input* [*options*]

NaNs are ignored in all statistics except for `count`. The output is formatted as [PST](https://github.com/peterkuma/pst).

**Arguments:**

- *var*: Variable name.
- *input*: Input file.
- *options*: See help for ds for global options.

**Output description:**

- `count`: Number of array elements.
- `max`: Maximum value.
- `mean`: Sample mean.
- `median`: Sample median.
- `min`: Minimum value.

**Examples:**

Print statistics of variable temperature in dataset.nc.

```
$ ds stats temperature dataset.nc
count: 3 min: 16.000000 max: 21.000000 mean: 18.333333 median: 18.000000
```

#### type

Print a variable type.

**Usage:** `ds type` *var* *input* [*options*]

**Arguments:**

- *var*: Variable to print the type of.
- *input*: Input file.
- *options*: See help for ds for global options.

**Examples:**

Print the type of a variable `temperature` in a dataset `dataset.nc`.

```
$ ds type temperature dataset.nc
float64
```

{% endraw %}