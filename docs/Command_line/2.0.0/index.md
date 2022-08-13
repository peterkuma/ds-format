---
layout: versioned
version: 2.0.0
title: Command line
---

## Command line

The ds-format Python package provides a command `ds` for reading, writing and
manipulating data files.

On Unix-like operating systems, manual pages are available for the commands
with `man ds` and `man ds` *cmd*.

### Synopsis

{% include cmd_ds.md %}

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
