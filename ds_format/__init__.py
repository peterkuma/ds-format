from .drivers.netcdf import from_netcdf, to_netcdf
from .op import select, get_dims, get_vars, time_dt, merge, copy, group_by, rename, rename_dim
from .io import read, readdir, index, write
from . import cmd
from . import misc
