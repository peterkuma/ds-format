import os
import h5py
import numpy as np
import ds_format as ds
from ds_format import misc

READ_EXT = ['h5', 'hdf5', 'hdf']
WRITE_EXT = ['h5', 'hdf5', 'hdf']

def detect(filename):
	try:
		with h5py.File(filename, 'r') as f:
			return True
	except:
		return False

def read_attrs(v, name=''):
	return {
		(name + '/' + k if name != '' else k): v
		for k, v in v.attrs.items()
	}

def read_var(f, var, name, sel=None, data=True):
	v = f[name]
	x = None
	attrs = read_attrs(v)
	if v.shape is None:
		dims = []
	else:
		dims = [
			var + ('_%d' % (i + 1)) if dim.label == '' else dim.label
			for i, dim in enumerate(v.dims)
		]
	size = v.shape
	type_ = misc.dtype_to_type(v.dtype)
	if data:
		if sel:
			s = ds.misc.sel_slice(sel, dims)
			x = v[s]
			dims = ds.misc.sel_dims(sel, dims)
		else:
			x = v[()] if v.ndim == 0 else v[::]
	if isinstance(x, h5py.Empty):
		x = None
	attrs.update({
		'.dims': dims,
		'.size': size,
		'.type': type_,
	})
	return [x, attrs]

def read_group(f, variables, sel, full):
	d = {}
	ds.attrs(d, None, read_attrs(f, f.name[1:]))
	for name in f.keys():
		if isinstance(f[name], h5py.Group):
			d1 = read_group(f[name], variables, sel, full)
			for k in d1.keys():
				if not k.startswith('.'):
					d[k] = d1[k]
			if '.' in d and '.' in d1:
				d['.'].update(d1['.'])
			elif '.' in d1:
				d['.'] = d1['.']
		else:
			prefix = f.name[1:]
			var = name if prefix == '' else prefix + '/' + name
			if variables is not None and var not in variables:
				if full:
					_, var_meta = read_var(f, var, name, sel, False)
					ds.meta(d, var, var_meta)
			else:
				data, var_meta = read_var(f, var, name, sel)
				ds.var(d, var, data)
				ds.meta(d, var, var_meta)
	return d

def read(filename, variables=None, sel=None, full=False, jd=False):
	with h5py.File(filename, 'r') as f:
		d = read_group(f, variables, sel, full)
	if jd:
		for var in ds.vars(d):
			misc.process_time_var(d, var)
	return d

def write(filename, d):
	ds.validate(d)
	with h5py.File(filename, 'w') as f:
		for var in ds.vars(d):
			data = ds.var(d, var)
			if data is None:
				dtype = misc.type_to_dtype(ds.type(d, var))
				f[var] = h5py.Empty(dtype)
			elif data.dtype.kind in ('U', 'O'):
				data2 = [
					x.encode('utf-8') if isinstance(x, str) else x
					for x in data.flatten()
				]
				data2 = np.array(data2).reshape(data.shape)
				f[var] = data2
			else:
				f[var] = data
			for i, dim in enumerate(ds.dims(d, var)):
				f[var].dims[i].label = dim
			for k, v in ds.attrs(d, var).items():
				f[var].attrs[k] = v
		for k, v in ds.attrs(d).items():
			path = k.split('/')
			if len(path) > 1:
				group = '/'.join(path[:-1])
				attr = path[-1]
				f[group].attrs[attr] = v
			else:
				f.attrs[k] = v
