from .drivers.netcdf import from_netcdf, to_netcdf
from .op import \
	copy, \
	get_attrs, \
	get_dims, \
	get_meta, \
	get_var, \
	get_vars, \
	group_by, \
	merge, \
	rename, \
	rename_dim, \
	select, \
	time_dt
from .io import read, readdir, index, write
from .validate import validate
from . import cmd
from . import misc
