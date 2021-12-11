import os
import re
from netCDF4 import Dataset
import cftime
import numpy as np
import ds_format as ds
import datetime as dt
import aquarius_time as aq

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
	for name in var.ncattrs():
		d[name] = var.getncattr(name)
	return d

def read_var(f, name, sel=None, data=True):
	var = f[name]
	x = None
	attrs = read_attrs(var)
	dims = var.dimensions
	size = var.shape
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
	})
	return [x, attrs]

def process_datetime_var(d, name):
	if not isinstance(d[name], np.ndarray):
		return
	x = d[name].flatten()
	if len(x) == 0:
		return
	shape = d[name].shape
	units = d['.'][name].get(u'units')
	calendar = d['.'][name].get(u'calendar', u'standard')
	if re.match(r'^days since -4712-01-01[T ]12:00(:00)?( UTC)?$', units) and \
	   calendar in (None, 'standard'):
		units = 'days since -4713-11-24 12:00 UTC'
		calendar = 'proleptic_gregorian'
	try:
		x = cftime.num2date(x, units,
			calendar=calendar,
			only_use_cftime_datetimes=False,
		)
	except: return
	if not (
		isinstance(x[0], cftime.real_datetime) or
		isinstance(x[0], cftime.datetime) or
		isinstance(x[0], dt.datetime)
	):
		return
	if isinstance(x[0], cftime.real_datetime) or \
	   isinstance(x[0], cftime.datetime):
		for i in range(len(x)):
			x[i] = dt.datetime(x[i].year, 1, 1) + \
			(x[i] - type(x[i])(x[i].year, 1, 1))
	d[name] = aq.from_datetime(list(x)).reshape(shape)
	d['.'][name]['units'] = 'days since -4713-11-24 12:00 UTC'
	d['.'][name]['calendar'] = 'proleptic_gregorian'

def read(filename, variables=None, sel=None, full=False, jd=False):
	if type(filename) is bytes and str != bytes:
		filename = os.fsdecode(filename)
	with Dataset(filename, 'r') as f:
		d = {}
		d['.'] = {}
		d['.']['.'] = read_attrs(f)
		for name in f.variables.keys():
			if variables is not None and name not in variables:
				if full:
					_, d['.'][name] = read_var(f, name, sel, False)
			else:
				d[name], d['.'][name] = read_var(f, name, sel)
	if jd:
		for name in ds.get_vars(d):
			process_datetime_var(d, name)
	return d

def write(filename, d):
	ds.validate(d)
	if type(filename) is bytes and hasattr(os, 'fsdecode'):
		filename = os.fsdecode(filename)
	with Dataset(filename, 'w') as f:
		dims = ds.get_dims(d)
		for k, v in dims.items():
			f.createDimension(k, v)
		for name in ds.get_vars(d):
			data = ds.get_var(d, name)
			if data.dtype == 'O' and \
				len(data.flatten()) > 0 and \
				type(data.flatten()[0]) is str:
				dtype = str
			else:
				dtype = data.dtype
			v = f.createVariable(name, dtype, ds.get_dims(d, name))
			v.setncatts(ds.get_attrs(d, name))
			v[::] = data
		f.setncatts(ds.get_attrs(d))

from_netcdf = read
to_netcdf = write
