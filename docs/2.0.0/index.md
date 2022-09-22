---
layout: default
title: About
---

## About

**ds-format is an open source program, a Python package and a storage format
which provides an interface for reading and writing NetCDF files, as well as its
own optional data file format. The data format and interface are a
simpler alternative to other more complex interfaces and formats, while
supporting most of the same essential functions.**

ds-format defines a structure storing data along with metadata, similar to
[NetCDF](https://www.unidata.ucar.edu/software/netcdf/) and 
[HDF](https://www.hdfgroup.org). It supports a subset
of functionality of NetCDF and is compatible with most existing NetCDF
datasets and the [CF Conventions](https://cfconventions.org/), if the necessary
attributes are defined in the dataset.

The ds-format Python package contains a command line program **ds** and a
Python module **ds_format**, which implement reading, writing and manipulation
of datasets. The package is designed so that functions are completely separated
from data, which is more transparent and faster than classes, especially when
working with large datasets.

Similar programs and libraries are [nco](http://nco.sourceforge.net/),
[CDO](https://code.mpimet.mpg.de/projects/cdo/)
[xarray](https://xarray.pydata.org) and
[iris](http://scitools.org.uk/iris/docs/latest/). Compatible programs
for viewing datasets include
[ncdump](https://www.unidata.ucar.edu/software/netcdf/),
[HDFView](https://www.hdfgroup.org/downloads/hdfview/) and
[Panoply](https://www.giss.nasa.gov/tools/panoply/).

### Development

Development is done under an open source MIT license. The repository is available
on [GitHub](https://github.com/peterkuma/ds-format). You can report bugs or
submit contributions on GitHub.
