import copy as copy_
import numpy as np
import datetime as dt
from . import misc

def select_var(d, name, sel):
	var_dims = list(d['.'][name]['.dims'])
	d['.'][name]['.dims'] = var_dims
	for key, value in sel.items():
		if type(value) == dict:
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
			idxs = np.array(idxs) if type(idxs) == list else idxs
			if isinstance(idxs, np.ndarray) and idxs.dtype == np.bool:
				idxs = np.nonzero(idxs)[0]
			if dim in var_dims:
				i = var_dims.index(dim)
				d[name] = np.take(d[name], idxs, axis=i)
				if not isinstance(idxs, np.ndarray):
					var_dims.remove(dim)

def select(d, sel):
	for name in d.keys():
		if name.startswith('.'):
			continue
		select_var(d, name, sel)

def get_dims(d):
	dims = {}
	for name in d.keys():
		if name.startswith('.'):
			continue
		for i, dim in enumerate(d['.'][name]['.dims']):
			dims[dim] = d[name].shape[i]
	return dims

def get_vars(d):
	return [x for x in d.keys() if not x.startswith('.')]

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

#def merge_var(dx, d, var, dim):
#	dimsx = dx['.'][var]['.dims']
#	dims = d['.'][var]['.dims']
#	if dims == dimsx and dim in dimsx:
#		i = dims.index(dim)
#		dx[var] = np.concatenate([dx[var], d[var]], axis=i)
#	else:
#		pass

def merge_var(dd, var, dim, new=False):
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
	elif new:
		meta['.dims'] = [dim] + list(meta['.dims'])
		x = np.stack([d[var] for d in dd if d['.'][var]['.dims'] == dims0])
	else:
		x = x0
		meta = meta0
	return x, meta

	# x = None
	# meta = None
	# for d in dd:
	# 	if new:
	# 		x0 = d[var][np.newaxis,...]
	# 		meta0 = copy.deepcopy(d['.'][var])
	# 		meta0['.dims'] = [dim] + list(d['.'][var]['.dims'])
	# 	else:
	# 		x0 = d[var]
	# 		meta0 = copy.deepcopy(d['.'][var])
	# 	if x is None:
	# 		x = x0
	# 		meta = meta0
	# 		continue
	# 	if meta['.dims'] == meta0['.dims'] and dim in meta['.dims']:
	# 		i = meta['.dims'].index(dim)
	# 		x = np.concatenate([x, x0], axis=i)
	# return x, meta

def merge(dd, dim, new=False):
	dx = {'.': {'.': {}}}
	vars_ = [x for d in dd for x in get_vars(d)]
	for var in vars_:
		x, meta = merge_var(dd, var, dim=dim, new=new)
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
