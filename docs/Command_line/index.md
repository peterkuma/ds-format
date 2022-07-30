---
layout: default
title: Command line
---

## Command line

The ds-format Python package provides a command `ds` for reading, writing and
manipulating data files.

### Synopsis

```
ds [<cmd>] [<options>]
ds --help [<cmd>]
```

Arguments:

- `cmd`: Command to execute or show help for. If omitted, the command `ls` is assumed.

Options:

- `--help`: Show a help message or help for a command.

The command line interface is based on the [PST format](https://github.com/peterkuma/pst).

### Commands

| Command | Description |
| --- | --- |
| [ls](#ls) | List variables. |
| [cat](#cat) | Print variable. |
| [get](#get) | Get attribute at a path. |
| [merge](#merge) | Merge files along a dimension. |
| [meta](#meta) | Print metadata. |
| [select](#select) | Select and subset variables. |
| [stats](#stats) | Print variable statistics. |
| [write](#write) | Write dataset to a file. |

{% include cmds.md %}
