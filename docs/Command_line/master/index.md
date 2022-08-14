---
layout: versioned
version: master
title: Command line
---

## Command line

The ds-format Python package provides a command `ds` for reading, writing and
manipulating data files.

The commands should be run in a shell such as Bash. zsh (the default shell on
macOS) is not well supported due to the fact that curly brackets are
interpreted as special characters in this shell. zsh can be used if curly
brackets are escaped with a backslash character (`\`).

On Unix-like operating systems, manual pages are available for the commands
with `man ds` and `man ds` *cmd*.

### Synopsis

{% include cmd_ds.md %}

### Commands

| Command | Description |
| --- | --- |
| [attrs](#attrs) | Print attributes in a dataset. |
| [cat](#cat) | Print variable. |
| [dims](#dims) | Print dimensions of a dataset or a variable. |
| [get](#get) | Get attribute at a path. |
| [ls](#ls) | List variables. |
| [merge](#merge) | Merge files along a dimension. |
| [meta](#meta) | Print dataset metadata. |
| [rename](#rename) | Rename variables and attributes. |
| [rename\_dim](#rename_dim) | Rename a dimension. |
| [rm](#rm) | Remove variables or attributes. |
| [select](#select) | Select and subset variables. |
| [set](#set) | Set variable data, dimensions and attributes in a dataset. |
| [stats](#stats) | Print variable statistics. |

{% include cmds.md %}
