{% raw %}#### apply

Apply a function on variables in a dataset.

**Usage:** `apply`(*d*, *func*, *dims*=`None`, *newdims*=`None`, *with_sel*=`False`)

Apply a function *func* on variables *vars*, or all variables if *vars* is `None`, in a dataset *d*. If *dims* is not `None`, the function is applied along dimensions *dims*. The function must return a scalar or an array of any number of dimensions. If the number of dimensions of the function result is smaller than the number of dimensions in *dims*, the surplus dimensions are removed. If the number is greater, additional dimensions are added adjacent to the last dimension of *dims*. *newdims* are the new dimensions to replace *dims*.

**Arguments:**

- *d*: Dataset (`dict`).
- *func*: Function to apply (`function`). The function signature is *f*(*x*) if *with_sel* is `False` or *f*(*x*, *sel*) if *with_sel* is `True`. *x* is a subset of the array along the dimensions *dims*. *sel* is a `dict` containing indexes of the subset, where the key is the dimension name and the value is the index.

**Options:**

- *dims*: Dimension name(s) (`str` or `list` of `str`).
- *newdims*: New dimension name(s) (`str` or `list` of `str`).
- *vars*: Variables to apply the function to, or all variables if `None`.
- *with_sel*: Pass a *sel* argument to *func* (`bool`).

**Return value:**

`None`

**Examples:**

Calculate mean of variables in a dataset *d*.

```
ds.apply(d, np.mean)
```

Calculate mean of variables along dimensions `x` and `y`.

```
ds.apply(d, np.mean, dims=['x', 'y'])
```

Interpolate variables in dataset *d* defined as 1D arrays with dimension `n` on irregular x- and y-coordinates given in variables *xg* (1D array) and *yg* (1D array) onto a regular grid defined by x- and y-coordinates *x* and *y*, and call the resulting dimensions `x` and `y`.

```
xm, ym = np.meshgrid(x, y)
ds.appply(d,
	lambda data: scipy.interpolate.griddata((xg, yg), data, (xm, ym),
	dims='n',
	newdims=['x', 'y']
)
```

#### attr

Get or set a dataset or variable attribute.

**Usage:** `attr`(*d*, *attr*, **value*, *var*=`None`)

**Arguments:**

- *d*: Dataset (`dict`).
- *attr*: Attribute name (`str`).
- *value*: Attribute value. If supplied, set the attribute value, otherwise get the attribute value.

**Options:**

- *var*: Variable name (`str`) to get or set a variable attribute, or `None` to get or set a dataset attribute.

**Return value:**

Attribute value if *value* is not set, otherwise `None`.

**Examples:**

Get an attribute `long_name` of a variable `temperature` in `dataset.nc`.

```
$ d = ds.read('dataset.nc')
ds.attr(d, 'long_name', var='temperature')
'temperature'
```

Get a dataset attribute `title` of `dataset.nc`.

```
$ ds.attr(d, 'title')
'Temperature data'
```

Set an attribute `units` of a variable `temperature` to `K`.

```
$ ds.attr(d, 'units', 'K', var='temperature')
$ ds.attr(d, 'units', var='temperature')
'K'
```

#### attrs

Get or set variable or dataset attributes.

**Usage:** `attrs`(*d*, *var*=`None`, **value*)

**Arguments:**

- *d*: Dataset (`dict`).
- *value*: Attributes to set (`dict`). If supplied, set attributes to *value*, otherwise get attributes.

**Options:**

- *var*: Variable name (`str`) or `None` to get dataset attributes.

**Return value:**

Attributes (`dict`).

**Examples:**

Get attributes of a variable `temperature` in a dataset `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}
```

Get dataset attributes.

```
$ ds.attrs(d)
{'title': 'Temperature data'}
```

Set attributes of a variable `temperature`.

```
$ ds.attrs(d, 'temperature', {'long_name': 'new temperature', 'units': 'K'})
$ ds.attrs(d, 'temperature')
{'long_name': 'new temperature', 'units': 'K'}
```

#### dim

Get a dimension size.

**Usage:** `dim`(*d*, *dim*, *full*=`None`)

**Arguments:**

- *d*: Dataset (`dict`).
- *dim*: Dimension name (`str`).

**Options:**

- *full*: Return dimension size also for a dimension for which no variable data are defined, i.e. it is only defined in dataset metadata.

**Return value:**

Dimension size or 0 if the dimension does not exist (`int`).

**Examples:**

Get the size of a dimension `time` in `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.dim(d, 'time')
3
```

Get the size of a dimension `time` in `dataset.nc` without reading data.

```
$ d = ds.read('dataset.nc', full=True)
$ ds.dim(d, 'time', full=True)
3
```

#### dims

**Aliases:**  get_dims


Get dataset or variable dimensions or set variable dimensions.

**Usage:** 

`dims`(*d*, *var*=`None`, **value*, *full*=`False`, *size*=`False`)<br />
`get_dims`(*d*, *var*=`None`, *full*=`False`, *size*=`False`)<br />


The function `get_dims` (deprecated) is the same as `dims`, but assumes that *size* is `True` if *var* is `None` and does not allow setting of dimensions.

**Arguments:**

- *d*: Dataset (`dict`).
- *value*: A list of dimensions (`list` of `str`) or `None`. If supplied, set variable dimensions, otherwise get dataset or variable dimensions. If `None`, remove variable dimensions (will be set to autogenerated names on write). If supplied, *var* must not be None.

**Options:**

- *var*: Variable name (`str`) or `None` to get dimensions for.
- *full*: Get variable dimensions even if the variable is only defined in the metadata (`bool`).
- *size*: Return a dictionary containing dimension sizes instead of a list.

**Return value:**

If *size* is `False`, a list of dataset or variable dimension names (`list` of `str`). If *size* is `True`, a dictionary of dataset or variable dimension names and sizes (`dict`), where a key is a dimension name (`str`) and the value is the dimension size (`int`). The order of keys in the dictionary is not guaranteed. Dataset dimensions are the dimensions of all variables together.

**Examples:**

Get dimensions of a dataset `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.dims(d)
['time']
```

Get dimension sizes.

```
$ ds.dims(d, size=True)
{'time': 3}
```

Get dimensions of a variable `temperature`.

```
$ ds.dims(d, 'temperature')
['time']
```

#### find

Find a variable, dimension or attribute matching a glob pattern in a dataset.

**Usage:** `find`(*d*, *what*, *name*, *var*=`None`)

If more than one name matches the pattern, raises `ValueError`.

**Arguments:**

- *d*: Dataset (`dict`).
- *what*: Type of item to find (`str`). One of: "var" (variable), "dim" (dimension), "attr" (attribute).
- *name*: [Glob pattern](https://docs.python.org/3/library/fnmatch.html) matching a variable, dimension or attribute name (`str`).

**Options:**

- *var*: Variable name (`str`) or `None`. Applies only if *what* is "attr". If not `None`, *name* is a variable attribute name, otherwise it is a dataset attribute name.

**Return value:**

A variable, dimension or attribute name matching the pattern, or *name* if no matching name is found (`str`).

**Examples:**

Find a variable matching the glob pattern `temp*` in a dataset `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.find(d, 'var', 'temp*')
'temperature'
```

#### findall

Find variables, dimensions or attributes matching a glob pattern in a dataset.

**Usage:** `findall`(*d*, *what*, *name*, *var*=`None`)

**Arguments:**

- *d*: Dataset (`dict`).
- *what*: Type of item to find (`str`). One of: "var" (variable), "dim" (dimension), "attr" (attribute).
- *name*: [Glob pattern](https://docs.python.org/3/library/fnmatch.html) matching a variable, dimension or attribute name (`str`).

**Options:**

- *var*: Variable name (`str`) or `None`. Applies only if *what* is "attr". If not `None`, *name* is a variable attribute name, otherwise it is a dataset attribute name.

**Return value:**

A list of variables, dimensions or attributes matching the pattern, or [*name*] if no matching names are found (`list` of `str`).

**Examples:**

Find all variables matching the glob pattern `t*` in a dataset `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.findall(d, 'var', 't*')
['temperature', 'time']
```

#### attrs

Get or set variable or dataset attributes.

**Usage:** `attrs`(*d*, *var*=`None`, **value*)

**Arguments:**

- *d*: Dataset (`dict`).
- *value*: Attributes to set (`dict`). If supplied, set attributes to *value*, otherwise get attributes.

**Options:**

- *var*: Variable name (`str`) or `None` to get dataset attributes.

**Return value:**

Attributes (`dict`).

**Examples:**

Get attributes of a variable `temperature` in a dataset `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}
```

Get dataset attributes.

```
$ ds.attrs(d)
{'title': 'Temperature data'}
```

Set attributes of a variable `temperature`.

```
$ ds.attrs(d, 'temperature', {'long_name': 'new temperature', 'units': 'K'})
$ ds.attrs(d, 'temperature')
{'long_name': 'new temperature', 'units': 'K'}
```

#### group_by

Group values along a dimension.

**Usage:** `group_by`(*d*, *dim*, *group*, *func*)

Each variable with a given dimension *dim* is split by *group* into subsets. Each subset is replaced with a value computed by *func*.

**Arguments:**

- *d*: Dataset (`dict`).
- *dim*: Dimension to group along (`str`).
- *group*: Groups (`ndarray` or `list`). Array of the same length as the dimension.
- *func*: Group function (`function`). *func*(*y*, axis=*i*) is called for each subset *y*, where *i* is the index of the dimension.

**Return value:**

`None`

**Examples:**

Calculate mean along a dimension `time` for a group where time <= 2 and a group where time > 2.

```
$ d = {
	'time': np.array([1., 2., 3., 4.]),
	'temperature': np.array([1., 3., 4., 6.]),
	'.': {
		'time': { '.dims': ['time'] },
		'temperature': { '.dims': ['time'] },
	}
}
$ ds.group_by(d, 'time', d['time'] > 2,  np.mean)
$ print(d['time'])
[1.5 3.5]
$ print(d['temperature'])
[1.5 3.5]
```

#### merge

Merge datasets along a dimension.

**Usage:** `merge`(*dd*, *dim*, *new*=`None`, *variables*=`None`, *jd*=`True`)

Merge datasets along a dimension *dim*. If the dimension is not defined in the dataset, merge along a new dimension *dim*. If *new* is `None` and *dim* is not new, variables without the dimension *dim* are set with the first occurrence of the variable. If *new* is not `None` and *dim* is not new, variables without the dimension *dim* are merged along a new dimension *new*. If *variables* is not `None`, only those variables are merged along a new dimension, and other variables are set to the first occurrence of the variable. Variables which are merged along a new dimension and are not present in all datasets have their subsets corresponding to the datasets where they are missing filled with missing values. Dataset and variable metadata are merged sequentially from all datasets, with metadata from later datasets overriding metadata from the former ones. When merging time variables whose units are not equal and *jd* is `True`, they are first converted to Julian date and then merged.

**Arguments:**

- *dd*: Datasets (`list`).
- *dim*: Name of a dimension to merge along (`str`).

**Options:**

- *new*: Name of a new dimension (`str`) or `None`.
- *variables*: Variables to merge along a new dimension (`list`) or `None` for all variables.
- *jd*: Convert time to Julian date when merging time variables with unequal units (`bool`).

**Return value:**

A dataset (`dict`).

**Examples:**

Merge datasets `d1` and `d2` along a dimension `time`.

```
$ d1 = {'time': [1, 2, 3], 'temperature': [16., 18., 21.], '.': {
	'time': { '.dims': ['time'] },
	'temperature': { '.dims': ['time'] },
}}
$ d2 = { 'time': [4, 5, 6], 'temperature': [23., 25., 28.], '.': {
	'time': { '.dims': ['time'] },
	'temperature': { '.dims': ['time'] },
}}
$ d = ds.merge([d1, d2], 'time')
$ print(d['time'])
[1 2 3 4 5 6]
$ print(d['temperature'])
[16. 18. 21. 23. 25. 28.]
```

#### meta

**Aliases:**  get_meta


Get or set dataset or variable metadata.

**Usage:** `meta`(*d*, *var*=`None`, **value*, *create*=`False`)

**Arguments:**

- *d*: Dataset (`dict`).

**Options:**

- *var*: Variable name (`str`), or `None` to get dataset metadata, or an empty string to get dataset attributes.
- *value*: Metadata to set (`dict`) or `None` to get metadata.
- *create*: Create (modifiable/bound) metadata dictionary in the dataset if not defined (`bool`). If `False`, the returned dictionary is an empty unbound dictionary if it is not already present in the dataset.

**Return value:**

Metadata (`dict`).

**Examples:**

Get metadata of a dataset `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ print(ds.meta(d))
{'.': {'title': 'Temperature data'}, 'temperature': {'long_name': 'temperature', 'units': 'celsius', '.dims': ('time',), '.size': (3,), '.type': 'float64'}, 'time': {'long_name': 'time', 'units': 's', '.dims': ('time',), '.size': (3,), '.type': 'int64'}}
```

Get metadata of a variable `temperature`.

```
$ ds.meta(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius', '.dims': ('time',), '.size': (3,), '.type': 'float64'}
```

Set metadata of a variable `temperature`.

```
$ ds.meta(d, 'temperature', { '.dims': ['new_time'], 'long_name': 'new temperature', 'units': 'K'})
$ ds.meta(d, 'temperature')
ds.meta(d, 'temperature', { '.dims': ['new_time'], 'long_name': 'new temperature', 'units': 'K'})
```

#### read

Read dataset from a file.

**Usage:** `read`(*filename*, *variables*=`None`, *sel*=`None`, *full*=`False`, *jd*=`False`)

**Arguments:**

- *filename*: Filename (`str`, `bytes` or `os.PathLike`).
- *variables*: Variable names to read (`str` or `list` of `str`) or `None` to read all variables.

**Options:**

- *sel*: Selector (see **[select](#select)**).
- *range_*: Select a dimension index range (see **[select](#select)**).
- *at*: Select based on variable values (see **[select](#select)**).
- *between*: Select based on a range between two variable values (see **[select](#select)**).
- *full*: Read all metadata (`bool`).
- *jd*: Convert time variables to Julian dates (see [Aquarius Time](https://github.com/peterkuma/aquarius-time)) (`bool`).

**Return value:**

Dataset (`dict`).

**Supported formats:**

- CSV/TSV: `.csv`, `.tsv`, `.tab`
- DS: `.ds`
- HDF5: `.h5`, `.hdf5`, `.hdf`
- JSON: `.json`
- NetCDF4: `.nc`, `.nc4`, `.nc3`, `.netcdf`

**Examples:**

Read a file `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ print(d.keys())
dict_keys(['.', 'temperature', 'time'])
$ print(d['temperature'])
[16. 18. 21.]
$ d['.']['temperature']
{'long_name': 'temperature', 'units': 'celsius', '.dims': ('time',), '.size': (3,), '.type': 'float64'}
```

Read a variable `temperature` at an index 0 of the dimension `time` from `dataset.nc`.

```
$ d = ds.read('dataset.nc', 'temperature', sel={'time': 0})
$ d.keys()
dict_keys(['.', 'temperature'])
$ print(d['temperature'])
16.0
```

Read only the metadata of `dataset.nc`.

```
$ d = ds.read('dataset.nc', [], full=True)
$ d.keys()
dict_keys(['.'])
$ print(d['.'])
{'.': {'title': 'Temperature data'}, 'temperature': {'long_name': 'temperature', 'units': 'celsius', '.dims': ('time',), '.size': (3,), '.type': 'float64'}, 'time': {'long_name': 'time', 'units': 's', '.dims': ('time',), '.size': (3,), '.type': 'int64'}}
```

#### readdir

Read all data files in a directory.

**Usage:** `readdir`(*dirname*, *variables*=`None`, *merge*=`None`, *warnings*=[], *recursive*=`False`, *parallel*=`False`, *executor*=`None`, *njobs*=`None`, ...)

Only files with known extensions are read. Files are read in an alphabetical order. Variable `filename` is added to the output datasets, containing the name of the file. If *merge* is not `None`, variables `i` and `n` are added to the resulting dataset, containing the index within the input dataset and a file index referring to the `filename` variable, respectively. They are defined along the dimension *merge* and are zero-indexed.

**Arguments:**

- *dirname*: Directory name (`str`, `bytes` or `os.PathLike`).

**Options:**

- *recursive*: If `True`, read the directory recursively (`bool`). Otherwise only files in the top-level directory are read.
- *variables*: Variable names to read (`str` or `list` of `str`) or `None` to read all variables.
- *merge*: Dimension name to merge datasets by (`str`) or `None`.
- *warnings*: A list to be populated with warnings (`list`).
- *parallel*: Enable parallel execution.
- *executor*: `concurrent.futures.Executor` instance or `None` to use a new executor.
- *njobs*: Number of parallel jobs or `None` to use the number of CPU cores.
- ...: Optional keyword arguments passed to **[read](#read)**.

**Return value:**

A list of datasets (`list` of `dict`) if *merge* is `None` or a merged dataset (`dict`) if *merge* is a dimension name.

**Supported formats:**

- CSV/TSV: `.csv`, `.tsv`, `.tab`
- DS: `.ds`
- HDF5: `.h5`, `.hdf5`, `.hdf`
- JSON: `.json`
- NetCDF4: `.nc`, `.nc4`, `.nc3`, `.netcdf`

**Examples:**

Read datasets `dataset1.nc` and `dataset2.nc` in the current directory (`.`).

```
$ ds.write('dataset1.nc', { 'time': [1, 2, 3], 'temperature': [16., 18., 21.], '.': {
	'time': { '.dims': ['time'] },
	'temperature': { '.dims': ['time'] },
}})
$ ds.write('dataset2.nc', { 'time': [4, 5, 6], 'temperature': [23., 25., 28.], '.': {
	'time': { '.dims': ['time'] },
	'temperature': { '.dims': ['time'] },
}})
$ dd = ds.readdir('.')
$ for d in dd: print(d['time'])
[1 2 3]
[4 5 6]
```

Read datasets in the current directory and merge them by a dimension `time`.

```
$ d = ds.readdir('.', merge='time')
$ print(d['time'])
[1 2 3 4 5 6]
$ print(d['temperature'])
[16. 18. 21. 23. 25. 28.]
```

#### rename

Rename a variable.

**Usage:** `rename`(*d*, *old*, *new*)

Any dimension with the same name is also renamed.

**Arguments:**

- *d*: Dataset (`dict`).
- *old*: Old variable name (`str`).
- *new*: New variable name (`str`) or `None` to remove the variable.

**Return value:**

`None`

**Examples:**

Rename a variable `temperature` to `new_temperature` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.vars(d)
['temperature', 'time']
$ ds.rename(d, 'temperature', 'new_temperature')
$ ds.vars(d)
['new_temperature', 'time']
```

#### rename_attr

Rename a dataset or variable attribute.

**Usage:** `rename_attr`(*d*, *old*, *new*, *var*=`None`)

**Arguments:**

- *d*: Dataset (`dict`).
- *old*: Old attribute name (`str`).
- *new*: New attribute name (`str`).

**Options:**

- *var*: Variable name (`str`) to rename a variable attribute or `None` to rename a dataset attribute.

**Return value:**

`None`

**Examples:**

Rename an attribute `units` of a variable `temperature` to `new_units` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}
$ ds.rename_attr(d, 'units', 'new_units', var='temperature')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'new_units': 'celsius'}
```

Rename a dataset attribute `title` to `new_title`.

```
$ ds.attrs(d)
{'title': 'Temperature data'}
$ ds.rename_attr(d, 'title', 'new_title')
$ ds.attrs(d)
{'new_title': 'Temperature data'}
```

#### rename_attr_m

Rename one or more dataset or variable attributes.

**Arguments:**

- *d*: Dataset (`dict`).
- *mapping*: A dictionary where the key is an old attribute name (`str`) and the value is a new attribute name (`str`) or `None` to remove the attribute. Swapping of atrributes is also supported.

**Options:**

- *var*: Variable name (`str`) to rename a variable attribute or `None` to rename a dataset attribute.

**Return value:**

`None`

**Examples:**

Rename an attribute `long_name` to `new_long_name` and `units` to `new_units` of a variable `temperature` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}
$ ds.rename_attr_m(d, {'long_name': 'new_long_name', 'units': 'new_units'}, var='temperature')
$ ds.attrs(d, 'temperature')
{'new_long_name': 'temperature', 'new_units': 'celsius'}
```

Rename a dataset attribute `title` to `new_title`.

```
$ ds.attrs(d)
{'title': 'Temperature data'}
$ ds.rename_attr_m(d, {'title': 'new_title'})
$ ds.attrs(d)
{'new_title': 'Temperature data'}
```

#### rename_dim

Rename a dimension.

**Usage:** `rename_dim`(*d*, *old*, *new*)

**Arguments:**

- *d*: Dataset (`dict`).
- *old*: Old dimension name (`str`).
- *new*: New dimension name (`str`).

**Return value:**

`None`

**Examples:**

Rename a dimension `time` to `new_time` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.dims(d)
['time']
$ ds.rename_dim(d, 'time', 'new_time')
$ ds.dims(d)
['new_time']
```

#### rename_dim_m

Rename one or more dimensions.

**Usage:** `rename_dim_m`(*d*, *mapping*)

**Arguments:**

- *d*: Dataset (`dict`).
- *mapping*: A dictionary where the key is an old dimension name (`str`) and the value is a new dimension name (`str`). Swapping of dimensions is also supported.

**Return value:**

`None`

**Examples:**

Rename a dimension `time` to `new_time` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.dims(d)
['time']
$ ds.rename_dim_m(d, {'time': 'new_time'})
$ ds.dims(d)
['new_time']
```

#### rename_m

Rename one or more variables.

**Usage:** `rename_m`(*d*, *mapping*)

Any dimension with the same name is also renamed.

**Arguments:**

- *d*: Dataset (`dict`).
- *mapping*: A dictionary where the key is an old variable name (`str`) and the value is a new variable name (`str`) or `None` to remove the variable. Swapping of variables is also supported.

**Return value:**

`None`

**Examples:**

Rename a variable `time` to `new_time` and `temperature` to `new_temperature` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.vars(d)
['temperature', 'time']
$ ds.rename(d, {'time': 'new_time', 'temperature': 'new_temperature'})
$ ds.vars(d)
['new_temperature', 'new_time']
```

#### require

Require that a variable, dimension or attribute is defined in a dataset.

**Usage:** `require`(*d*, *what*, *name*, *var*=`None`, *full*=`False`)

If the item is not found and the mode is "soft", returns `False`. If the mode is "strict", raises `NameError`. If the mode is "moderate", produces a warning and returns `False`.

**Arguments:**

- *d*: Dataset (`dict`).
- *what*: Type of item to require. One of: "var" (variable), "dim" (dimension), "attr" (attribute) (`str`).
- *name*: Variable, dimension or attribute name (`str`).

**Options:**

- *var*: Variable name (`str`) or `None`. Applies only if *what* is "attr". If not `none`, *name* is a variable attribute name, otherwise it is a dataset attribute name.
- *full*: Also look for items which are defined only in dataset metadata (`bool`).

**Return value:**

`True` if the required item is defined in the dataset, otherwise `False` or raises an exception depending on the mode.

**Examples:**

Require that a variable `temperature` is defined in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.require(d, 'var', 'temperature')
True
```

#### rm

Remove a variable.

**Usage:** `rm`(*d*, *var*)

**Arguments:**

- *d*: Dataset (`dict`).
- *var*: Variable name (`str`).

**Return value:**

`None`

**Examples:**

Remove a variable `temperature` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.vars(d)
['temperature', 'time']
$ ds.rm(d, 'temperature')
$ ds.vars(d)
['time']
```

#### rm_attr

Remove a dataset or variable attribute.

**Usage:** `rm_attr`(*d*, *attr*, *var*)

**Arguments:**

- *d*: Dataset (`dict`).
- *attr*: Attribute name (`str`).

**Options:**

- *var*: Variable name (`str`) to remove a variable attribute or `None` to remove a dataset attribute.

**Return value:**

`None`

**Examples:**

Remove an attribute `long_name` of a variable `temperature` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}
$ ds.rm_attr(d, 'long_name', var='temperature')
$ ds.attrs(d)
{'title': 'Temperature data'}
```

Remove a dataset attribute `title` in a dataset read from `dataset.nc`.

```
$ ds.attrs(d)
{'title': 'Temperature data'}
$ ds.rm(d, 'title')
$ ds.attrs(d)
{}
```

#### select

Filter dataset by a selector.

**Usage:** `select`(*d*, *sel*=`None`, *range_*=`None`, *at*=`None`, *between*=`None`)

The function subsets data of all variables in a dataset *d* by a selectors *sel*, *range_*, *at*, and *between*. If multiple of the selectors are used, the resulting selector is an intersection of all of them.

**Arguments:**

- *d*: Dataset (`dict`).

**Options:**

- *sel*: Selector (`dict`). The selector is a dictionary where the key is a dimension name (`str`) and the value is a mask, a list of indexes (`list` or `np.array`) or an index (`int`) to subset by along the dimension.
- *range_*: Range selector (`dict`). The range selector is a dictionary where the key is a dimension name (`str`) and the value is a pair (`list`, `tuple`, or `np.ndarray`) of indexes (`int`) for the start and the end of the range. If the index is `None`, the range is from the start or to the end of the dimension, respectively. Negative index values are counted from the end of the dimension. The range start is inclusive (closed), and the end is exclusive (open).
- *at*: At selector (`dict`). The at selector is a dictionary where the key is a variable name (`str`) and the value is value or a list (`list`, `tuple`, or `np.ndarray`) of values. The dimension indexes corresponding the variable are constrained so that a variable value closest to the value is selected.
- *between*: Between selector (`dict`). The between selector is a dictionary where the key is a variable name (`str`) and the value a pair of values for the start and the end of a range. The dimension indexes corresponding to the variable are constrained so that variable values in the range are selected. If the value is `None`, the range start or end is unlimited. The range start is inclusive (closed), and the end is exclusive (open).

**Return value:**

`None`

**Examples:**

Subset index 0 a along dimension `time` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.var(d, 'temperature')
print(ds.var(d, 'temperature'))
$ ds.select(d, {'time': 0})
$ ds.var(d, 'temperature')
16
```

Subset by a mask along a dimension `time` in a dataset read from `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.select(d, {'time': [False, True, True]})
$ ds.var(d, 'temperature')
[18. 21.]
```

#### size

Get variable size.

**Usage:** `size`(*d*, *var*)

Variable size is determined based on the size of the variable data if defined, or by variable metadata attribute `.size`.

**Arguments:**

- *d*: Dataset (`dict`).
- *var*: Variable name (`str`).

**Return value:**

Variable size (`list`) or `None` if not defined.

**Examples:**

Get the size of a variable `temperature` in `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.size(d, 'temperature')
[3]
```

#### split

Split a dataset along one or more dimensions.

**Usage:** `split`(*d*, *dims*)

**Arguments:**

- *d*: Dataset (`dict`).
- *dims*: Dimension name (`str`) or a list of dimension names (`list` of `str`).

**Return value:**

List of datasets (`list` of `dict`).

#### type

Get or set variable type.

**Usage:** `type`(*d*, *var*, **value*)

Variable type is determined based on the type of the variable data if defined, or by variable metadata attribute `.type`.

**Arguments:**

- *d*: Dataset (`dict`).
- *var*: Variable name (`str`).
- *value*: Variable type (`str`). One of: `float32` and `float64` (32-bit and 64-bit floating-point number, resp.), `int8`, `int16`, `int32` and `int64` (8-bit, 16-bit, 32-bit and 64-bit integer, resp.), `uint8`, `uint16`, `uint32` and `uint64` (8-bit, 16-bit, 32-bit and 64-bit unsigned integer, resp.), `bool` (boolean), `str` (string) and `unicode` (Unicode).

**Return value:**

Variable type (`str`) or `None` if not defined.

**Examples:**

Get the type of a variable `temperature` in `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.type(d, 'temperature')
'float64'
```

Set the type of a variable `temperature` to `int64`.

```
$ ds.type(d, 'temperature', 'int64')
$ ds.type(d, 'temperature')
'int64'
$ print(ds.var(d, 'temperature'))
[16 18 21]
```

#### var

Get or set variable data.

**Usage:** `var`(*d*, *var*, **value*)

Variable to get or set is normalized in the following way. If the variable data are a `list` or `tuple`, they are converted to `np.ndarray`, or to `np.ma.MaskedArray` if they contain `None`, which is masked. If the variable data are `int`, `float`, `bool`, `str`, `bytes` or `np.array` with zero dimensions, they are converted to `np.generic`.

**Arguments:**

- *d*: Dataset (`dict`).
- *var*: Variable name (`str`).
- *value*: Variable data. If supplied, set variable data, otherwise get variable data.

**Return value:**

Variable data (`np.ndarray`, `np.ma.MaskedArray`, `np.generic` or `np.ma.core.MaskedConstant`) or `None` if the variable data are not defined or `value` is supplied.  Raises `ValueError` if the output dtype is not one of the types `np.float32`, `np.float64`, `np.int8`, `np.int16`, `np.int32`, `np.int64`, `np.uint8`, `np.uint16`, `np.uint32`, `np.uint64`, `np.bool`, `np.bytes<n>`, `np.str<n>`, or `np.object` for which all items are an instance of `str` or `bytes`.

**Examples:**

Get data of a variable `temperature` in a dataset `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ print(ds.var(d, 'temperature'))
[16. 18. 21.]
```

Set data of a variable `temperature`.

```
$ ds.var(d, 'temperature', [17, 18, 22])
$ ds.var(d, 'temperature')
array([17, 18, 22])
```

#### vars

**Aliases:**  get_vars


Get all variable names in a dataset.

**Usage:** `get_vars`(*d*, *full*=`False`)

**Arguments:**

- *d*: Dataset (`dict`).

**Options:**

- *full*: Also return variable names which are only defined in the metadata.

**Return value:**

Variable names (`list` of `str`).

**Examples:**

List variables in a dataset `dataset.nc`.

```
$ d = ds.read('dataset.nc')
$ ds.vars(d)
['temperature', 'time']
```

List variables in a dataset `dataset.nc` without reading the data.

```
$ d = ds.read('dataset.nc', [], full=True)
$ ds.vars(d, full=True)
['temperature', 'time']
```

#### with_mode

Context manager which temporarily changes ds.mode.

**Arguments:**

- *mode*: Mode to set (`str`). See **[mode](#mode)**.

**Examples:**

A block of code in which ds.mode is set to "soft".

```
with ds.with_mode('soft'):
	...
```

#### write

Write dataset to a file.

**Usage:** `write`(*filename*, *d*)

The file type is determined from the file extension.

**Arguments:**

- *filename*: Filename (`str`, `bytes` or `os.PathLike`).
- *d*: Dataset (`dict`).

**Return value:**

`None`

**Supported formats:**

- CSV/TSV: `.csv`, `.tsv`, `.tab`
- DS: `.ds`
- HDF5: `.h5`, `.hdf5`, `.hdf`
- JSON: `.json`
- NetCDF4: `.nc`, `.nc4`, `.netcdf`

**Examples:**

Write a dataset to a file `dataset.nc`.

```
$ ds.write('dataset.nc', {
	'time': [1, 2, 3],
	'temperature': [16. 18. 21.],
})
```

Write a dataset with metadata to a file `dataset.nc`.

```
$ ds.write('dataset.nc', {
	'time': [1, 2, 3],
	'temperature': [16. 18. 21.],
	'.': {
		'.': { 'title': 'Temperature data' },
		'time': { '.dims': ['time'] },
		'temperature': { '.dims': ['time'], 'units': 'degree_celsius' },
	}
})
```

{% endraw %}