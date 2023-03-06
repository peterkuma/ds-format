---
layout: default
title: Installation
---

## Installation

Installation on Linux is recommended, but it is also known to work on Windows
and macOS. On macOS the command line interface should be used with bash, not
the default zsh, which is not compatible with the syntax.

Requirements:

- Python 3, or a Python distribution such
as [Anaconda](https://www.anaconda.com/distribution/)

To install ds-format and dependencies:

```
pip3 install ds-format
```

If installing as a non-root user on Linux, you might have to add
`$HOME/.local/bin` to the PATH environment variable in `~/.profile` (or an
equivalent configuration file) in order to be able to run the `ds` command,
and `$HOME/.local/share/man` to MANPATH in order to have access to the manual
pages.

### Release notes

{% include releasenotes.md %}
