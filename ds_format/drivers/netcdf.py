import os
from netCDF4 import Dataset
import numpy as np
import ds_format as ds
from ds_format import misc

JD_UNITS = 'days since -4713-11-24 12:00 UTC'
JD_CALENDAR = 'proleptic_greogorian'

READ_EXT = ['nc', 'nc4', 'nc3', 'netcdf', 'hdf', 'h5']
WRITE_EXT = ['nc', 'nc4', 'netcdf']

def detect(filename):
	try:
		f = Dataset(filename)
		return True
	except:
		return False

def read_attrs(var):
	d = {}
	for attr in var.ncattrs():
		d[attr] = var.getncattr(attr)
	return d

def read_var(f, name, sel=None, data=True):
	var = f[name]
	x = None
	attrs = read_attrs(var)
	dims = var.dimensions
	size = var.shape
	type_ = misc.dtype_to_type(var.dtype)
	if data:
		if sel:
			s = ds.misc.sel_slice(sel, dims)
			x = var[s]
			dims = ds.misc.sel_dims(sel, dims)
		else:
			try:
				x = var[::] if data else None
			except ValueError:
				var.set_auto_mask(False)
				x = var[::] if data else None
	attrs.update({
		'.dims': dims,
		'.size': size,
		'.type': type_,
	})
	return [x, attrs]

def read(filename, variables=None, sel=None, full=False, jd=False):
	if type(filename) is bytes and str != bytes:
		filename = os.fsdecode(filename)
	with Dataset(filename, 'r') as f:
		d = {}
		ds.attrs(d, None, read_attrs(f))
		for var in f.variables.keys():
			if variables is not None and var not in variables:
				if full:
					_, var_meta = read_var(f, var, sel, False)
					ds.meta(d, var, var_meta)
			else:
				data, var_meta = read_var(f, var, sel)
				ds.var(d, var, data)
				ds.meta(d, var, var_meta)
	if jd:
		for var in ds.vars(d):
			misc.process_time_var(d, var)
	return d

def write(filename, d):
	ds.validate(d)
	if type(filename) is bytes and hasattr(os, 'fsdecode'):
		filename = os.fsdecode(filename)
	with Dataset(filename, 'w') as f:
		dims = ds.dims(d, size=True)
		for k, v in dims.items():
			f.createDimension(k, v)
		for var in ds.vars(d):
			data = ds.var(d, var)
			if data.dtype == 'O' and \
				len(data.flatten()) > 0 and \
				type(data.flatten()[0]) is str:
				dtype = str
			else:
				dtype = data.dtype
			v = f.createVariable(var, dtype, ds.dims(d, var))
			v.setncatts(ds.attrs(d, var))
			v[::] = data
		f.setncatts(ds.attrs(d))

from_netcdf = read
to_netcdf = write
