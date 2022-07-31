---
layout: default
title: Installation
---

## Installation

Installation on Linux is recommended, but it is also known to work on Windows
and macOS.

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

#### 2.0.0 (2022-07-31)

- Command line documentation and man pages.
- Command output in PST format.
- ds ls: Added `a:` *attrs* option.
- New ds file format (experimental).
- Documentation website.

#### 1.1.2 (2022-01-01)

- Fixed handling of NetCDF time variables.
- Fixed merge function definition and implementation.

#### 1.1.1 (2021-12-11)

- Dataset validation on write.
- Dropped support for Python 2.
- merge: new variables option.

#### 1.1.0 (2021-03-31)

- Improved reading of NetCDF time variables.
- Documented readdir function.

#### 1.0.1 (2020-08-12)

- Dependencies installed from PyPI.

#### 1.0.0 (2020-04-28)

- Initial release.
