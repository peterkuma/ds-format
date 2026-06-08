{% raw %}#### ds

Tool for reading, writing and modifying dataset files.

**Usage:** 

`ds` [*cmd* [*args*]] [*options*] [*read_options*] [*write_options*]<br />
`ds --help` [*cmd*]<br />
`ds --version`<br />


The command line interface is based on the [PST format](https://github.com/peterkuma/pst). In all commands, variable, dimension and attribute names are interpreted as [glob patterns](https://docs.python.org/3/library/fnmatch.html), unless the `-F` option is enabled. Note that the pattern has to be enclosed in quotes in order to prevent the shell from interpreting the glob.

**Arguments:**

- *cmd*: Command to execute or show help for. If omitted, `ds` is a shorthand for the command `ls`, with a difference that files with the same name as any available command cannot be listed. Available commands are listed below.
- *args*: Command arguments and options.

**Options:**

- `-F`: Interpret variable, dimension and attribute names as fixed strings instead of glob patterns.
- `--help`: Show this help message or help for a command if *cmd* is supplied.
- `-j`: Print command output as JSON instead of [PST](https://github.com/peterkuma/pst).
- `-m`: Moderate error handling mode. Report a warning on missing variables, dimensions and attributes. Overrides the DS_MODE environment variable.
- `--noindent`: Disable output indentation.
- `-s`: Strict error handling mode. Handle missing variables, dimensions and attributes as errors. Overrides the DS_MODE environment variable.
- `-t`: Soft error handling mode. Ignore missing variables, dimensions and attributes. Overrides the DS_MODE environment variable.
- `-v`: Be verbose. Print more detailed information and error messages.
- `--version`: Print the version number and exit.

**Available commands:**

- `attrs`: Print attributes in a dataset.
- `cat`: Print variable data.
- `dim`: Print dimension size.
- `dims`: Print dimensions of a dataset or a variable.
- `ls`: List variables.
- `merge`: Merge files along a dimension.
- `meta`: Print dataset metadata.
- `rename`: Rename variables and attributes.
- `rename_dim`: Rename a dimension.
- `rm`: Remove variables or attributes.
- `select`: Select and subset variables.
- `set`: Set variable data, dimensions and attributes in an existing or new dataset.
- `size`: Print variable size.
- `stats`: Print variable statistics.
- `type`: Print variable type.

**Supported input formats:**

- CSV/TSV: `.csv`, `.tsv`, `.tab`
- DS: `.ds`
- HDF5: `.h5`, `.hdf5`, `.hdf`
- JSON: `.json`
- NetCDF4: `.nc`, `.nc4`, `.nc3`, `.netcdf`

**Supported output formats:**

- CSV/TSV: `.csv`, `.tsv`, `.tab`
- DS: `.ds`
- HDF5: `.h5`, `.hdf5`, `.hdf`
- JSON: `.json`
- NetCDF4: `.nc`, `.nc4`, `.netcdf`

**Read options:**

- `at:` *selector*: At selector as `{` *var*`:` *value* ... `}` or `{` *var*`:` `{` *value*... `}` ... `}`, where *value* is the value of the variable *var* to select. The dimension indexes corresponding the variable are constrained so that a variable value closest to the value is selected.
- `between:` *selector*: Between selector as `{` *var*`: {` *start* *end* `}` ... `}`, where *start* is the start value of the variable *var*, and *end* is the end value. The dimension indexes corresponding to the variable are constrained so that variable values in the range are selected. If the value is `none`, the range start or end is unlimited. The range start is inclusive (closed), and the end is exclusive (open).
- `range:` *selector*: Range selector as `{` *dim*`: {` *start* *end* `}` ... `}`, where *start* is the start index of the dimension *dim*, and *end* is the end index. If the index is `none`, the range is from the start or to the end of the dimension, respectively. Negative index values are counted from the end of the dimension. The range start is inclusive (closed), and the end is exclusive (open).
- `sel:` *selector*: Selector as *dim*`:` *idx* pairs, where *dim* is a dimension name and *idx* is an index or a list of indexes as `{` *i*... `}`.

**Write options:**

- `calendar:` *value*: CF-Conventions calendar to use for time variables when writing NetCDF4 and HDF5 files.
- `time_units:` *value*: CF-Conventions units to use for time variables when writing NetCDF4 and HDF5 files.

**Environment variables:**

- DS_MODE: Error handling mode. If "strict", handle missing variables, dimensions and attributes as errors. If "moderate", report a warning. If "soft", ignore missing items.

{% endraw %}