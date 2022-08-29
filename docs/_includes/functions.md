{% raw %}#### attr

Get or set a dataset or variable attribute.

Usage: `attr`(*d*, *name*, **value*, *var*=`None`)

Arguments:

- *d*: Dataset (`dict`).
- *name*: Attribute name (`str`).
- *value*: Attribute value. If supplied, set the attribute value, otherwise get the attribute value.

Options:

- *var*: Variable name (`str`) to get or set a variable attribute, or `None` to get or set a dataset attribute.

Return value:

Attribute value if *value* is not set, otherwise `None`.

#### attrs

Get variable or dataset attributes.

Usage: `attrs`(*d*, *var*=`None`)

Arguments:

- *d*: Dataset (`dict`).

Options:

- *var*: Variable name (`str`) or `None` to get dataset attributes.

Return value:

Attributes (`dict`).

#### dim

Get a dimension size.

Usage: `dim`(*d*, *name*, *full*=`None`)

Arguments:

- *d*: Dataset (`dict`).
- *name*: Dimension name (`str`).

Options:

- *full*: Return dimension size also for a dimension for which no variable data are defined, i.e. it is only defined in dataset metadata.

Return value:

Dimension size or 0 if the dimension does not exist (`int`).

#### dims

Aliases:  get_dims


Get dataset or variable dimensions or set variable dimensions.

Usage: `dims`(*d*, *name*=`None`, **value*, *full*=`False`, *size*=`False`)

Arguments:

- *d*: Dataset (`dict`).
- *value*: A list of dimensions (`list` of `str`). If supplied, set variable dimensions, otherwise get dataset or variable dimensions.

Options:

- *name*: Variable name (`str`).
- *full*: Get variable dimensions even if the variable is only defined in the matadata (`bool`).
- *size*: Return a dictionary containing dimension sizes.

Return value:

Dimension names (`list` of `str`) or a dictionary of dimension sizes (`dict`).

#### attrs

Get variable or dataset attributes.

Usage: `attrs`(*d*, *var*=`None`)

Arguments:

- *d*: Dataset (`dict`).

Options:

- *var*: Variable name (`str`) or `None` to get dataset attributes.

Return value:

Attributes (`dict`).

#### group_by

Group values along a dimension.

Usage: `group_by`(*d*, *dim*, *group*, *func*)

Each variable with a given dimension *dim* is split by *group* into subsets. Each subset is replaced with a value computed by *func*.

Arguments:

- *d*: Dataset (`dict`).
- *dim*: Dimension to group along (`str`).
- *group*: Groups (`ndarray` or `list`). Array of the same length as the dimension.
- *func*: Group function (`function`). *func*(*y*, axis=*i*) is called for each subset *y*, where *i* is the index of the dimension.

Return value:

`None`

#### merge

Merge datasets along a dimension.

Usage: `merge`(*dd*, *dim*, *new*=`None`, *variables*=`None`)

Merge datasets along a dimension *dim*. If the dimension is not defined in the dataset, merge along a new dimension *dim*. If *new* is None and *dim* is not new, variables without the dimension are set with the first occurrence of the variable. If *new* is not None and *dim* is not new, variables without the dimension *dim* are merged along a new dimension *new*. If *variables* is not None, only those variables are merged along a new dimension and other variables are set to the first occurrence of the variable.

Arguments:

- *dd*: Datasets (`list`).
- *dim*: Name of a dimension to merge along (`str`).

Options:

- *new*: Name of a new dimension (`str`) or `None`.
- *variables*: Variables to merge along a new dimension (`list`) or `None` for all variables.

Return value:

A dataset (`dict`).

#### meta

Aliases:  get_meta


Get dataset or variable metadata.

Usage: `meta`(*d*, *var*=`None`, *create*=`False`)

Arguments:

- *d*: Dataset (`dict`).

Options:

- *var*: Variable name (`str`), or `None` to get dataset metadata, or an empty string to get dataset attributes.
- *create*: Create (modifyable/bound) metadata dictionary in the dataset if not defined (`bool`). If `False`, the returned dictionary is an empty unbound dictionary if not present in the dataset.

Return value:

Metadata (`dict`).

#### read

Read dataset from a file.

Usage: `read`(*filename*, *variables*=`None`, *sel*=`None`, *full*=`False`, *jd*=`False`)

Arguments:

- *filename*: Filename (`str`).
- *variables*: Variable names to read (`list` of `str`).

Options:

- *sel*: Selector (see **[select](#select)**).
- *full*: Read all metadata (`bool`).
- *jd*: Convert time variables to Julian dates (see [Aquarius Time](https://github.com/peterkuma/aquarius-time)) (`bool`).

Return value:

Dataset (`dict`).

Supported formats:

- DS: `.ds`
- JSON: `.json`
- NetCDF4: `.nc`, `.nc4`, `.nc3`, `.netcdf`, `.hdf`, `.h5`

#### readdir

Read multiple files in a directory.

Usage: `readdir`(*dirname*, *variables*=`None`, *merge*=`None`, *warnings*=[], ...)

Arguments:

- *dirname*: Directory name.

Options:

- *variables*: Variable names to read (`list` of `str`).
- *merge*: Dimension name to merge datasets by.
- *warnings*: Array to be populated with warnings.
- ...: Optional keyword arguments passed to **[read](#read)**.

Return value:

A list of datasets (`list` of `dict`) if *merge* is `None` or a merged dataset (`dict`) if *merge* is a dimension name.

#### rename

Rename a variable.

Usage: `rename`(*d*, *old*, *new*)

Any dimension with the same name is also renamed.

Arguments:

- *d*: Dataset (`dict`).
- *old*: Old variable name (`str`).
- *new*: New variable name (`str`).

Return value:

`None`

#### rename_attr

Rename a dataset or variable attribute.

Arguments:

- *d*: Dataset (`dict`).
- *old*: Old attribute name (`str`).
- *new*: New attribute name (`str`).

Options:

- *var*: Variable name (`str`) to rename a variable attribute or `None` to rename a dataset attribute.

Return value:

`None`

#### rename

Rename a dimension.

Usage: `rename_dim`(*d*, *old*, *new*)

Arguments:

- *d*: Dataset (`dict`).
- *old*: Old variable name (`str`).
- *new*: New variable name (`str`).

Return value:

`None`

#### rm

Remove a variable.

Usage: `rm`(*d*, *var*)

Arguments:

- *d*: Dataset (`dict`).
- *name*: Variable name (`str`).

Return value:

`None`

#### rm_attr

Remove a dataset or variable attribute.

Usage: `rm_attr`(*d*, *attr*, *var*)

Arguments:

- *d*: Dataset (`dict`).
- *name*: Attribute name (`str`).

Options:

- *var*: Variable name (`str`) to remove a variable attribute or `None` to remove a dataset attribute.

Return value:

`None`

#### select

Filter dataset by a selector.

Usage: `select`(*d*, *sel*)

Arguments:

- *d*: Dataset (`dict`).
- *sel*: Selector (`dict`). Selector is a dictionary where each key is a dimension name and value is a mask to apply along the dimension or a list of indexes.

Return value:

`None`

#### var

Get or set variable data.

Usage: `var`(*d*, *name*, **value*)

Arguments:

- *d*: Dataset (`dict`).
- *name*: Variable name (`str`).
- *value*: Variable data. If supplied, set variable data, otherwise get variable data.

Return value:

Variable data as a numpy array (`np.ndarray`) or `None` if the variable data are not defined or `value` is supplied.

#### vars

Aliases:  get_vars


Get all variable names in a dataset.

Usage: `get_vars`(*d*, *full*=`False`)

Arguments:

- *d*: Dataset (`dict`).

Options:

- *full*: Also return variable names which are only defined in the metadata.

Return value:

Variable names (`list` of `str`).

#### write

Write dataset to a file.

Usage: `write`(*filename*, *d*)

The file type is determined from the file extension.

Arguments:

- *filename*: Filename (`str`).
- *d*: Dataset (`dict`).

Return value:

`None`

Supported formats:

- NetCDF4: `.nc`, `.nc4`, `.netcdf`
- JSON: `.json`
- DS: `.ds`

{% endraw %}