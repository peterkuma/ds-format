from collections import Mapping, Iterable
import copy as copy_
import numpy as np
import datetime as dt
from . import misc

def select_var(d, name, sel):
	var_dims = list(d['.'][name]['.dims'])
	d['.'][name]['.dims'] = var_dims
	for key, value in sel.items():
		if isinstance(value, Mapping):
			if len(sel) > 1: raise ValueError('invalid selector')
			newdim = key
			dims = value.keys()
			idxs = value.values()
			selector = tuple([
				idxs[dims.index(var_dim)] if var_dim in dims else slice(None)
				for var_dim in var_dims
			])
			d[name] = d[name][selector]
			for dim in dims:
				if dim in var_dims:
					var_dims.remove(dim)
			d['.'][name]['.dims'].append(newdim)
		else:
			dim, idxs = key, value
			idxs = np.array(idxs) if type(idxs) in (list, tuple) else idxs
			if isinstance(idxs, np.ndarray) and idxs.dtype == np.bool:
				idxs = np.nonzero(idxs)[0]
			if dim in var_dims:
				i = var_dims.index(dim)
				d[name] = np.take(d[name], idxs, axis=i)
				if not isinstance(idxs, np.ndarray):
					var_dims.remove(dim)

def filter_hidden(x):
	if isinstance(x, Mapping):
		return {k: v for k, v in x.items() if not k.startswith('.')}
	if isinstance(x, Iterable):
		return [k for k in x if not k.startswith('.')]
	return x

def select(d, sel):
	for name in d.keys():
		if name.startswith('.'):
			continue
		select_var(d, name, sel)

def get_dims(d, name=None):
	if name is None:
		dims = {}
		for name in get_vars(d):
			data = get_var(d, name)
			for i, dim in enumerate(get_dims(d, name)):
				dims[dim] = data.shape[i]
		return dims
	else:
		try: return d['.'][name]['.dims']
		except KeyError: return gen_dims(d, name)

def get_vars(d):
	return filter_hidden(d.keys())

def get_var(d, name):
	data = d[name]
	if type(data) is np.ndarray:
		return data
	else:
		return np.array(data)

def get_meta(d, name=None):
	if name is None:
		return d.get('.', {})
	else:
		try: return d['.'][name]
		except KeyError: return {}

def get_attrs(d, name=None):
	if name is None:
		try: return filter_hidden(d['.']['.'])
		except KeyError: return {}
	else:
		try: return filter_hidden(d['.'][name])
		except KeyError: return {}

def gen_dims(d, name):
	data = get_var(d, name)
	return [name + ('_%d' % i) for i in range(1, data.ndim + 1)]

def parse_time(t):
	formats = [
		'%Y-%m-%d %H:%M:%S.%f',
		'%Y-%m-%d %H:%M:%S',
		'%Y-%m-%dT%H:%M:%SZ',
	]
	for f in formats:
		try: return dt.datetime.strptime(t, f)
		except: pass
	return None

def time_dt(time):
	return [parse_time(t) for t in time]

def merge_var(dd, var, dim):
	if len(dd) == 0:
		return None, None
	x0 = dd[0][var]
	meta0 = dd[0]['.'][var]
	dims0 = meta0['.dims']
	meta = copy_.deepcopy(meta0)
	if dim in dims0:
		i = dims0.index(dim)
		x = np.concatenate(
			[d[var] for d in dd if d['.'][var]['.dims'] == dims0],
			axis=i
		)
	else:
		meta['.dims'] = [dim] + list(meta['.dims'])
		x = np.stack([d[var] for d in dd if d['.'][var]['.dims'] == dims0])
	return x, meta

def merge(dd, dim, new=False, variables=None):
	dx = {'.': {'.': {}}}
	vars_ = [x for d in dd for x in get_vars(d)]
	dims = [k for d in dd for k in get_dims(d).keys()]
	new = dim not in dims
	for var in vars_:
		if (new and (variables is None or var in variables)) or \
		   dim in get_dims(dd[0], var):
			x, meta = merge_var(dd, var, dim=dim)
		else:
			x, meta = dd[0][var], dd[0]['.'][var]
		dx[var] = x
		dx['.'][var] = meta
	for d in dd:
		if '.' in d['.']:
			dx['.']['.'].update(d['.']['.'])
	return dx

def rename_dim(d, old, new):
	if old == new:
		return
	if '.' in d:
		for var in d['.'].keys():
			meta = d['.'][var]
			if '.dims' in d['.'][var]:
				dims = d['.'][var]['.dims']
				for i, dim in enumerate(dims):
					if dim == old:
						dims[i] = new

def rename(d, old, new):
	if old == new:
		return
	if old in d:
		d[new] = d[old]
		d['.'][new] = d['.'][old]
		del d[old]
		del d['.'][old]
	rename_dim(d, old, new)

def copy(d):
	d2 = {}
	for var in get_vars(d):
		d2[var] = d[var]
	d2['.'] = copy_.deepcopy(d['.'])
	return d2

def group_by(d, dim, group, func):
	groups = sorted(list(set(group)))
	vars = get_vars(d)
	n = len(groups)
	for var in vars:
		dims = d['.'][var]['.dims']
		try:
			i = dims.index(dim)
		except ValueError:
			continue
		size = list(d[var].shape)
		size[i] = n
		x = np.empty(size, d[var].dtype)
		for j, g in enumerate(groups):
			mask = group == g
			slice_x = misc.sel_slice({dim: j}, dims)
			slice_y = misc.sel_slice({dim: mask}, dims)
			y = d[var][slice_y]
			x[slice_x] = func(y, axis=i)
		d[var] = x
