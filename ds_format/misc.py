import ds_format as ds
import numpy as np
from contextlib import contextmanager

KIND_TO_TYPE = {
	'f': 'float',
	'i': 'int',
	'u': 'uint',
	'b': 'bool',
	'U': 'unicode',
	'S': 'str',
}

TYPE_TO_DTYPE = {
	'float32': np.float32,
	'float64': np.float64,
	'int8': np.int8,
	'int16': np.int16,
	'int32': np.int32,
	'int64': np.int64,
	'uint8': np.uint8,
	'uint16': np.uint16,
	'uint32': np.uint32,
	'uint64': np.uint64,
	'bool': np.bool,
	'str': np.str,
	'unicode': np.unicode,
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
	return '\\' + name \
		if name is not None and name.startswith(('.', '\\')) \
		else name

def unescape(name):
	return name[1:] \
		if name is not None and name.startswith(('\\.', '\\\\')) \
		else name

def dtype_to_type(dtype):
	type_ = None
	if dtype is bytes:
		return 'str'
	if dtype is str:
		return 'unicode'
	elif dtype.kind in KIND_TO_TYPE:
		type_ = KIND_TO_TYPE[dtype.kind]
	elif dtype.kind == 'O':
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
	tmp = ds.mode
	ds.mode = mode
	yield
	ds.mode = tmp
