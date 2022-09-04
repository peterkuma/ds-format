{% raw %}#### ds

Tool for reading, writing and modifying dataset files.

Usage: 

`ds` [*cmd* [*args*]] [*options*]<br />
`ds --help` [*cmd*]<br />
`ds --version`<br />


The command line interface is based on the [PST format](https://github.com/peterkuma/pst). In all commands, variable, dimension and attribute names are interpreted as [glob patterns](https://docs.python.org/3/library/fnmatch.html), unless the `-F` option is enabled. Note that the pattern has to be enclosed in quotes in order to prevent the shell from interpreting the glob.

Arguments:

- *cmd*: Command to execute or show help for. If omitted, `ds` is a shorthand for the command `ls`, with a difference that files with the same name as any available command cannot be listed. Available commands are listed below.
- *args*: Command arguments and options.

Options:

- `-F`: Interpret variable, dimension and attribute names as fixed strings, not glob patterns.
- `--help`: Show this help message or help for a command.
- `-m`: Moderate error handling mode. Report a warning on missing variables, dimensions and attributes.
- `-s`: Strict error handling mode. Handle missing variables, dimensions and attributes as errors. Overrides DS_MODE environment variable.
- `-t`: Soft error handling mode. Ignore missing variables, dimensions and attributes. Overrides DS_MODE environment variable.
- `-v`: Be verbose. Print more detailed information and error messages.
- `--version`: Print the version number and exit.

Available commands:

- `attrs`: Print attributes in a dataset.
- `cat`: Print variable data.
- `dims`: Print dimensions of a dataset or a variable.
- `ls`: List variables.
- `merge`: Merge files along a dimension.
- `meta`: Print dataset metadata.
- `rename`: Rename variables and attributes.
- `rename_dim`: Rename a dimension.
- `rm`: Remove variables or attributes.
- `select`: Select and subset variables.
- `set`: Set variable data, dimensions and attributes in an existing or new dataset.
- `stats`: Print variable statistics.

Supported input formats:

- DS: `.ds`
- JSON: `.json`
- NetCDF4: `.nc`, `.nc4`, `.nc3`, `.netcdf`, `.hdf`, `.h5`

Supported output formats:

- DS: `.ds`
- JSON: `.json`
- NetCDF4: `.nc`, `.nc4`, `.netcdf`

Environment variables:

- DS_MODE: Error handling mode. If `strict`, handle missing variables, dimensions and attributes as errors. If `moderate`, report a warning. If `soft`, ignore missing items.

{% endraw %}