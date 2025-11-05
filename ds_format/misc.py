import datetime as dt
import json
import ds_format as ds
import numpy as np
from contextlib import contextmanager
import re
import cftime
import aquarius_time as aq
import pst

KIND_TO_TYPE = {
	'f': 'float',
	'i': 'int',
	'u': 'uint',
	'b': 'bool',
	'U': 'unicode',
	'S': 'str',
}

TYPE_TO_DTYPE = {
	'float32': np.dtype('float32'),
	'float64': np.dtype('float64'),
	'int8': np.dtype('int8'),
	'int16': np.dtype('int16'),
	'int32': np.dtype('int32'),
	'int64': np.dtype('int64'),
	'uint8': np.dtype('uint8'),
	'uint16': np.dtype('uint16'),
	'uint32': np.dtype('uint32'),
	'uint64': np.dtype('uint64'),
	'bool': np.dtype('bool'),
	'str': np.dtype('object'),
	'unicode': np.dtype('object'),
}

def sel_slice(sel, dims):
	return tuple([
		slice(None) if dim not in sel.keys() else sel[dim]
		for dim in dims
	])

def sel_dims(sel, dims):
	return [
		dim
		for dim in dims
		if dim not in sel.keys() or \
			isinstance(sel[dim], np.ndarray) or \
			type(sel[dim]) in (list, tuple)
	]

def sel_from_range(d, range_):
	def norm(side, x, dim):
		if x is None:
			return 0 if side == 1 else ds.dim(d, dim)
		elif x >= 0:
			return x
		else:
			return ds.dim(d, dim) + x
	return {
		dim: np.arange(norm(1, r[0], dim), norm(2, r[1], dim), dtype=int)
		for dim, r in range_.items()
	}

def sel_from_at(d, at):
	sel = {}
	for var, v in at.items():
		sel_var = {}
		dims = ds.dims(d, var)
		def process(x):
			if isinstance(x, str):
				x = aq.from_iso(x)
				res = get_time_var(d, var)
				if res is not None:
					data = res[0]
			else:
				data = ds.var(d, var)
			ii = np.argmin(np.abs(data - x))
			if len(dims) <= 1:
				ii = [ii]
			for dim, i in zip(dims, ii):
				sel_var[dim] = np.union1d(sel_var[dim], i) \
					if dim in sel_var else i
		if isinstance(v, np.ndarray) or type(v) in (list, tuple):
			[process(v1) for v1 in v]
		else:
			process(v)
		for dim, v in sel_var.items():
			sel[dim] = np.intersect1d(sel[dim], v) \
				if dim in sel else v
	return sel

def sel_from_between(d, between):
	sel = {}
	for var, b in between.items():
		for i, b1 in enumerate([b[0], b[1]]):
			if isinstance(b1, str):
				b1 = aq.from_iso(b1)
				res = get_time_var(d, var)
				if res is not None:
					data = res[0]
			else:
				data = ds.var(d, var)
			if i == 0:
				mask = data >= b1 \
					if b1 is not None else np.ones(data.shape, bool)
			else:
				mask &= data < b1 \
					if b1 is not None else np.ones(data.shape, bool)
		ii = np.where(mask)[0]
		sel[var] = ii
	return sel

def sel_merge(sels):
	sel = {}
	for sel1 in sels:
		if sel1 is None: continue
		for dim, ii in sel1.items():
			sel[dim] = np.intersect1d(sel[dim], ii) if dim in sel else ii
	return sel

def sel_from_any(d, sel, range_, at, between):
	sel_range = sel_from_range(d, range_) if range_ is not None else None
	sel_at = sel_from_at(d, at) if at is not None else None
	sel_between = sel_from_between(d, between) if between is not None else None
	return sel_merge([sel, sel_range, sel_at, sel_between])

def encoder(x):
	if isinstance(x, np.generic):
		return x.item()
	elif isinstance(x, np.ma.MaskedArray) or \
		isinstance(x, np.ma.core.MaskedConstant):
		return x.tolist(None)
	elif isinstance(x, np.ndarray):
		return x.tolist()
	else:
		return x

def escape(name):
	check(name, 'name', [str, None])
	return '\\' + name \
		if name is not None and name.startswith(('.', '\\')) \
		else name

def unescape(name):
	check(name, 'name', [str, None])
	return name[1:] \
		if name is not None and name.startswith(('\\.', '\\\\')) \
		else name

def dtype_to_type(dtype, data=None):
	type_ = None
	if dtype is bytes:
		return 'str'
	if dtype is str:
		return 'unicode'
	elif dtype.kind in KIND_TO_TYPE:
		type_ = KIND_TO_TYPE[dtype.kind]
	elif dtype.kind == 'O' and data is not None:
		if isinstance(data, bytes) or \
		   isinstance(data, np.ndarray) and \
		   all([isinstance(x, bytes) for x in data.flatten()]):
			type_ = 'str'
		else:
			type_ = 'unicode'
	else:
		return None
	if type_ in ['bool', 'str', 'unicode']:
		return type_
	else:
		return '%s%d' % (type_, dtype.itemsize*8)

def type_to_dtype(type_):
	return TYPE_TO_DTYPE.get(type_)

@contextmanager
def with_mode(mode):
	'''
	title: with_mode
	caption: "Context manager which temporarily changes ds.mode."
	arguments: {{
		*mode*: "Mode to set (`str`). See **[mode](#mode)**."
	}}
	examples: {{
		"A block of code in which ds.mode is set to \\"soft\\".":
"with ds.with_mode('soft'):
	..."
	}}
	'''
	check(mode, 'mode', str)
	tmp = ds.mode
	ds.mode = mode
	yield
	ds.mode = tmp

def cf_time_raw(data, meta):
	if not isinstance(data, (np.ndarray, np.generic)):
		return
	x = data.flatten()
	if len(x) == 0:
		return
	shape = data.shape
	units = meta.get('units')
	calendar = meta.get('calendar', 'standard')
	if units is not None and isinstance(units, str) and \
	   re.match(r'^days since -4712-01-01[T ]12:00(:00)?( UTC)?$', units) and \
	   calendar in (None, 'standard'):
		units = 'days since -4713-11-24 12:00 UTC'
		calendar = 'proleptic_gregorian'
	mask = ~np.ma.getmaskarray(x)
	try: mask &= np.isfinite(x)
	except: pass
	if np.sum(mask) == 0:
		return
	try:
		y = cftime.num2date(x[mask], units,
			calendar=calendar,
			only_use_cftime_datetimes=False,
		)
		x = x.astype(np.object_)
		x[mask] = y
	except: return
	x0 = x[mask][0]
	if not (
		isinstance(x0, cftime.real_datetime) or
		isinstance(x0, cftime.datetime) or
		isinstance(x0, dt.datetime)
	):
		return
	if isinstance(x0, cftime.real_datetime) or \
	   isinstance(x0, cftime.datetime):
		for i in range(len(x)):
			if not mask[i]:
				continue
			x[i] = dt.datetime(x[i].year, 1, 1) + \
			(x[i] - type(x[i])(x[i].year, 1, 1))
	x = [aq.from_datetime(x[i]) if mask[i] else x[i] for i in range(len(x))]
	return np.array(x).reshape(shape), \
		'days since -4713-11-24 12:00 UTC', \
		'proleptic_gregorian'

def cf_time(data, meta, units=None, calendar=None):
	if not meta.get('.time'):
		return
	var_units = meta.get('units', 'days since -4713-11-24 12:00 UTC')
	var_calendar = meta.get('calendar', 'proleptic_gregorian')
	if (
		(units is None or var_units == units) and \
		(calendar is None or var_calendar == calendar)
	):
		return data, var_units, var_calendar
	x = data.flatten()
	shape = data.shape
	mask = ~np.ma.getmaskarray(x)
	y = cftime.num2date(x[mask], var_units, var_calendar)
	x = cftime.date2num(y, units, calendar)
	x = x.astype(float)
	return np.array(x).reshape(shape), units, calendar

def process_cf_time_var(d, var):
	data = ds.var(d, var)
	meta = ds.meta(d, var)
	res = cf_time_raw(data, meta)
	if res:
		data, units, calendar = res
		ds.var(d, var, data)
		ds.attr(d, 'units', units, var=var)
		ds.attr(d, 'calendar', calendar, var=var)
		ds.time(d, var, True)

def check(x, name, arg, *args, elemental=False, fail=True):
	if type(x) is tuple:
		x = list(x)
	ta = type(arg)
	if ta not in (list, tuple):
		arg = [[arg] + list(args)]
	res = False
	for a in arg:
		if type(a) not in (list, tuple):
			a = [a]
		if x is None and a[0] is None or \
		   a[0] is not None and isinstance(x, a[0]):
			if a[0] in (list, tuple) and len(a) >= 2:
				res = all([
					check(y, name, a[1], elemental=elemental, fail=False) \
					for y in x
				])
			elif a[0] is dict and len(a) >= 2:
				if len(a) == 2:
					res = all([
						check(k, name, a[1], elemental=elemental, fail=False)
						for k, v in x.items()
					])
				else:
					res = all([
						check(k, name, a[1], elemental=elemental, fail=False) and \
						check(v, name, a[2], elemental=elemental, fail=False) \
						for k, v in x.items()
					])
			else:
				res = True
	if not res and fail:
		raise ValueError('%s: invalid type' % name)
	return res

class UsageError(TypeError):
	pass

class JSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.generic):
			return obj.item()
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		if isinstance(obj, bytes):
			return obj.decode('utf-8', 'surrogateencoding')
		return super().default(obj)

def encode(x):
	if ds.output == 'json':
		return json.dumps(x, cls=JSONEncoder, indent=4).encode('utf-8')
	else:
		return pst.encode(x, encoder=encoder, indent=True)
