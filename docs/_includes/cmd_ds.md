{% raw %}#### ds

Tool for reading, writing and modifying dataset files.

Usage: 

`ds` [*cmd* [*args*]]<br />
`ds --help` [*cmd*]<br />
`ds --version`<br />


The command line interface is based on the [PST format](https://github.com/peterkuma/pst).

Arguments:

- *cmd*: Command to execute or show help for. If omitted, `ds` is a shorthand for the command `ls`, with a difference that files with the same name as any available command cannot be listed. Available commands are listed below.
- *args*: Command arguments and options.

Options:

- `--help`: Show this help message or help for a command.
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

{% endraw %}