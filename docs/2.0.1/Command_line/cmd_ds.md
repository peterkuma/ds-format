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

- `ls`: List variables.
- `cat`: Print variable.
- `get`: Get attribute at a path.
- `merge`: Merge files along a dimension.
- `meta`: Print metadata.
- `select`: Select and subset variables.
- `stats`: Print variable statistics.
- `write`: Write dataset to a file.

{% endraw %}