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
	'str': np.dtype('str'),
	'unicode': np.dtype('unicode'),
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
		if all([type(x) is bytes for x in data.flatten()]):
			type_ = 'str'
		elif all([type(x) is str for x in data.flatten()]):
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

def process_time_var(d, var):
	data = ds.var(d, var)
	if not isinstance(data, np.ndarray):
		return
	x = data.flatten()
	if len(x) == 0:
		return
	shape = data.shape
	attrs = ds.attrs(d, var)
	units = attrs.get('units')
	calendar = attrs.get('calendar', 'standard')
	if units is not None and \
	   re.match(r'^days since -4712-01-01[T ]12:00(:00)?( UTC)?$', units) and \
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
	ds.var(d, var, aq.from_datetime(list(x)).reshape(shape))
	ds.attr(d, 'units', 'days since -4713-11-24 12:00 UTC', var=var)
	ds.attr(d, 'calendar', 'proleptic_gregorian', var=var)

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
			return list(obj)
		if isinstance(obj, bytes):
			return obj.decode('utf-8', 'surrogateencoding')
		return super().default(obj)

def encode(x):
	if ds.output == 'json':
		return json.dumps(x, cls=JSONEncoder, indent=4).encode('utf-8')
	else:
		return pst.encode(x, encoder=encoder, indent=True)
