---
layout: default
title: Installation
---

{% assign pkg = 'https://github.com/peterkuma/ds-format/archive/refs/heads/master.zip' %}

## Installation

Installation on Linux is recommended, but it is also known to work on Windows
and macOS.

**Important:** On macOS the ds command should be used with the command line
shell bash, not the default zsh, which is not compatible with the argument
syntax.

### Linux

1. Install the required system packages. On Debian-derived distributions
   (Ubuntu, Devuan, ...):

   ```
   apt install python3-full python3-pip pipx
   ```

   On Fedora:

   ```
   sudo yum install python3 python3-pip pipx
   ```

2. Install ds format. If you indend to use the command-line interface, you can
   install ds format with pipx:

   ```
   pipx install {{ pkg }}
   ln -s ~/.local/pipx/venvs/ds-format/share/man/man1/ds*.1 ~/.local/share/man/man1/
   ```

   You might have to add `$HOME/.local/bin` to the PATH environment variable
   if not present already in order to access the ds command. This can be done
   with `pipx ensurepath`.

   If you indend to use the Python interface, you can install in the home
   directory with pip3:

   ```
   pip3 install {{ pkg }}
   ```

   Replace pip3 with pip if pip3 is not available. Add `--break-system-packages`
   if your distribution does not allow installing into the home directory but
   you want to anyway.

   Alternatively, install into a Python virtual environment with:

   ```
   python3 -m venv venv
   . venv/bin/activate
   pip3 install {{ pkg }}
   ```

   You can then use the ds format Python interface from within the virtual
   environment. Deactivate the environment with `deactivate`.

### Windows

1. Install [Python](https://www.python.org/). In the installer, tick `Add
python.exe to PATH`.

2. Open the Command Prompt from the Start menu. Install ds format with:

    ```
	pip3 install {{ pkg }}
	```

### macOS

Open the Terminal. Install ds format with:

```
python3 -m pip install {{ pkg }}
```

### Uninstallation

To uninstall if installed with pipx:

```
pipx uninstall ds-format
rm ~/.local/pipx/venvs/ds-format/share/man/man1/ds*.1
```

To uninstall if installed with pip3 or pip:

```
pip3 uninstall ds-format
```

Replace pip3 with pip if pip3 is not available.

### Release notes

{% include releasenotes.md %}
