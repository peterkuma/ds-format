{% raw %}#### ds

Tool for reading, writing and manipulating dataset files.

Usage: 

`ds` [*cmd*] [*options*]<br />
`ds --help` [*cmd*]<br />
`ds --version`<br />


The command line interface is based on the [PST format](https://github.com/peterkuma/pst).

Arguments:

- *cmd*: Command to execute or show help for. If omitted, the command `ls` is assumed. Available commands are listed below.

Options:

- `--help`: Show this help message or help for a command.
- `--version`: Print the version number and exit.

Available commands:

- `attrs`: Print attributes in a dataset.
- `cat`: Print variable.
- `dims`: Print dimensions of a dataset or a variable.
- `get`: Get attribute at a path.
- `ls`: List variables.
- `merge`: Merge files along a dimension.
- `meta`: Print dataset metadata.
- `rm`: Remove variables.
- `rename`: Rename variables.
- `rename_attr`: Rename an attribute in a dataset.
- `rename_dim`: Rename a dimension.
- `select`: Select and subset variables.
- `set`: Set or add variable data, dimensions and attributes in an existing dataset.
- `set_attrs`: Set attributes in a dataset.
- `set_dims`: Set variable dimensions.
- `stats`: Print variable statistics.
- `write`: Write dataset to a file.

{% endraw %}