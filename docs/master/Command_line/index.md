---
layout: default
title: Command line
---

## Command line

The ds-format Python package provides a command `ds` for reading, writing and
modifying data files.

The command should be run in a shell such as Bash. zsh (the default shell on
macOS) is not well supported due to the fact that curly brackets (`{`, `}`) are
interpreted as special characters in this shell. zsh can be used if curly
brackets are escaped with a backslash character (`\`).

On Unix-like operating systems, manual pages are available for the commands
with `man ds` and `man ds` *cmd*. Note that you might have to add the manual
page path (usually `$HOME/.local/share/man/`) to the `MANPATH` environment
variable in order to access the manual pages.

### Synopsis

{% include_relative cmd_ds.md %}

### Commands

| Command | Description |
| --- | --- |
| [attrs](#attrs) | Print attributes in a dataset. |
| [cat](#cat) | Print variable data. |
| [dims](#dims) | Print dimensions of a dataset or a variable. |
| [ls](#ls) | List variables. |
| [merge](#merge) | Merge files along a dimension. |
| [meta](#meta) | Print dataset metadata. |
| [rename](#rename) | Rename variables and attributes. |
| [rename\_dim](#rename_dim) | Rename a dimension. |
| [rm](#rm) | Remove variables or attributes. |
| [select](#select) | Select and subset variables. |
| [set](#set) | Set variable data, dimensions and attributes in an existing or new dataset. |
| [size](#size) | Print a variable size. |
| [stats](#stats) | Print variable statistics. |
| [type](#type) | Print a variable type. |

{% include_relative cmds.md %}
