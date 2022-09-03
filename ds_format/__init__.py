__version__ = '2.0.0'

import os
mode = os.environ.get('DS_MODE', 'soft')

from .drivers.netcdf import from_netcdf, to_netcdf
from .op import \
	attr, \
	attrs, \
	copy, \
	dim, \
	dims, \
	find, \
	findall, \
	get_attrs, \
	get_dims, \
	get_meta, \
	get_vars, \
	group_by, \
	merge, \
	meta, \
	rename, \
	rename_dim, \
	rename_attr, \
	require, \
	rm, \
	rm_attr, \
	select, \
	var, \
	vars_ as vars, \
	time_dt
from .io import read, readdir, index, write
from .validate import validate
from . import cmd
from . import misc
