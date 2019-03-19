import copy
import numpy as np
import datetime as dt

def select_var(d, name, sel):
	var_dims = list(d['.'][name]['.dims'])
	d['.'][name]['.dims'] = var_dims
	for key, value in sel.iteritems():
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
			if type(idxs) == np.ndarray and idxs.dtype == np.bool:
				idxs = np.nonzero(idxs)[0]
			if dim in var_dims:
				i = var_dims.index(dim)
				d[name] = np.take(d[name], idxs, axis=i)
				if type(idxs) != np.ndarray:
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
	x = None
	meta = None
	for d in dd:
		if new:
			x0 = d[var][np.newaxis,...]
			meta0 = copy.deepcopy(d['.'][var])
			meta0['.dims'] = [dim] + list(d['.'][var]['.dims'])
		else:
			x0 = d[var]
			meta0 = copy.deepcopy(d['.'][var])
		if x is None:
			x = x0
			meta = meta0
			continue
		if meta['.dims'] == meta0['.dims'] and dim in meta['.dims']:
			i = meta['.dims'].index(dim)
			x = np.concatenate([x, x0], axis=i)
	return x, meta

def merge(dd, dim, new=False):
	dx = {'.': {}}
	vars_ = [x for d in dd for x in get_vars(d)]
	for var in vars_:
		x, meta = merge_var(dd, var, dim=dim, new=new)
		dx[var] = x
		dx['.'][var] = meta
	return dx

def rename(d, old, new):
	d[new] = d[old]
	d['.'][new] = d['.'][old]
	del d[old]
	del d['.'][old]
