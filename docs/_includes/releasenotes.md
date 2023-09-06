#### 4.0.0 (2023-09-06)

- The ds command is now installed using setuptools entry_points, which also
  works on Windows.
- ds.var: Normalize variable data when setting the variable.
- Imporved documentation.
- CSV: Fixes in file reading when some columns are not defined.
- ds.split: New function for splitting datasets.
- netcdf: Fixed missing JD_UNITS and JD_CALENDAR.
- ds cat: New -n option for disabling header.
- Support for .tab/.tsv format.

#### 3.7.0 (2023-04-24)

- ds rename, ds rename\_dim: Fix renaming  multiple vars, attrs or dims at a time.
- ds.rename\_m, ds.rename\_attr\_m, ds.rename\_dim\_m: New function.
- ds.rename: Also remove variable metadata.
- ds.readdir: Fix warnings.
- Fixes in the documentation.

#### 3.6.1 (2023-04-21)

- ds.readdir: Fixed handling of unreadable files.
- ds.attr: Fixed getting attr when var does not exist.
- Fixes in the documentation.

#### 3.6.0 (2023-04-01)

- Support for parallel processing in readdir.
- Fixed merging of time variables by ds merge.
- Do not show SIGPIPE error message when sending output to another command.
- ds stats: NaNs are now ignored in the calculation of statistics.
- ds stats: Output standard deviation and confidence intervals.
- Improved documentation.

#### 3.5.2 (2023-03-06)

- Fixed an issue with a new version of NumPy.

#### 3.5.1 (2022-11-30)

- Fixed installation location for manual pages.

#### 3.5.0 (2022-11-26)

- merge: Fixed handling of missing variables.
- type: Fixed handling of string variables.
- hdf: Fixed handling of type of string variables.
- Minor fixes and improvements in documentation.

#### 3.4.0 (2022-11-22)

- readdir: Added recursive option.
- Improved documentation.

#### 3.3.3 (2022-11-13)

- Fixed storing of missing values.

#### 3.3.2 (2022-11-13)

- Fixed setting of dataset attributes in the ds storage format.

#### 3.3.1 (2022-11-10)

- Fixed package imports in new Python.
- Fixed missing required package.
- Minor improvements in the documentation.

#### 3.3.0 (2022-10-16)

- Basic support for CSV.
- Improved documentation.
- meta: Argument naming more consistent with the rest of the API.
- group_by: Fixed argument checking.
- Fixed JSON encoding of NumPy arrays.

#### 3.2.0 (2022-10-09)

- Support for HDF5.
- Fixes in ds cat JSON output.
- Fixes in the NetCDF driver.

#### 3.1.0 (2022-10-05)

- Support for JSON output in commands.

#### 3.0.0 (2022-09-30)

- New commands and Python API functions.
- Version 1.0 of the storage format (incompatible with the previous experimental format).
- Support for empty variables.
- pst output in commands instead of JSON.
- Improved argument checking.
- Improved documentation and command help.
- Support for variables beginning with a dot (in the ds storage format).
- Improved support for missing values.
- Glob pattern matching of variable, attribute and dimension names in commands.
- Support for error reporting modes.

#### 2.0.1 (2022-09-26)

- Fixed missing package in setup.py (Markdown).

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
