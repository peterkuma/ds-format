import sys
import json
from copy import copy
import numpy as np
import ds_format as ds

READ_EXT = ['ds']
WRITE_EXT = ['ds']

TYPES = {
	'f': 'float',
	'i': 'int',
	'u': 'uint',
	'b': 'bool',
	'U': 'unicode',
	'S': 'str',
}

class JSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.generic):
			return obj.item()
		if isinstance(obj, np.ndarray):
			return list(obj)
		return json.JSONEncoder(self, obj)

def read(filename, variables=None, sel=None, full=False, jd=False):
	d = {}
	with open(filename, 'rb') as f:
		header = f.readline()
		meta_s = header.decode('utf-8')
		meta = json.loads(meta_s)
		d['.'] = meta
		data_offset = len(header)
		if variables is not None and not full:
			meta = {k: v for k, v in meta.items() if k in variables}
		for name in meta.keys():
			if name.startswith('.') or \
			   variables is not None and name not in variables:
				continue
			var = meta[name]
			if not ('.offset' in var and \
			   		'.type' in var and \
			   		'.dsize' in var and \
			   		'.len' in var and \
			   		'.size' in var and \
					'.endian' in var):
				continue
			if var['.type'] in ['float', 'int', 'uint']:
				dt = np.dtype('%s%d' % (var['.type'], var['.dsize']))
			elif var['.type'] in ['bool']:
				dt = np.dtype(var['.type'])
			elif var['.type'] == 'str':
				dt = np.bytes_
			elif var['.type'] == 'unicode':
				dt = np.unicode_
			else:
				continue
			byteorder = {
				'l': '<',
				'b': '>',
			}[var['.endian']]
			dt = dt.newbyteorder(byteorder)
			count = np.prod(var['.size'])
			if var['.type'] in ('str', 'unicode'):
				len_ = 64*count
			else:
				len_ = int(np.ceil(count*var['.dsize']/8))
			f.seek(data_offset + var['.offset'])
			if var['.type'] == 'bool':
				data = np.fromfile(f, 'uint8', count=len_)
				data = np.unpackbits(data)[:count]
				data = data.astype(bool)
			elif var['.type'] in ('str', 'unicode'):
				dt_slen = np.dtype('uint64').newbyteorder(byteorder)
				slen = np.fromfile(f, dt_slen, count=count)
				data = []
				for slen1 in slen:
					if var['.type'] == 'str':
						data += [f.read(slen1)]
					else:
						data += [f.read(slen1).decode('utf-8')]
				data = np.array(data, 'O')
			else:
				data = np.fromfile(f, dt, count=count)
			if var['.size'] == 1:
				data = data[0]
			else:
				data = data.reshape(var['.size'])

			if sel is not None:
				dims = ds.get_dims(d, name)
				s = ds.misc.sel_slice(sel, dims)
				dims = ds.misc.sel_dims(sel, dims)
				var['.dims'] = dims
				data = data[s]
			if var.get('.missing') is True:
				mask_len = int(np.ceil(count/8))
				f.seek(data_offset + var['.offset'] + len_)
				mask = np.fromfile(f, 'uint8', count=mask_len)
				mask = np.unpackbits(mask)[:count]
				mask = mask.reshape(var['.size'])
				if sel is not None:
					s = ds.misc.sel_slice(sel, dims)
					mask = mask[s]
				data = np.ma.array(data, mask=mask)
			d[name] = data
	return d

def write(filename, d):
	ds.validate(d)
	offset = 0
	meta = {}
	for name in ds.get_vars(d):
		var = copy(ds.get_meta(d, name))
		data = ds.get_var(d, name)
		if data.shape == ():
			var['.size'] = 1
		else:
			var['.size'] = data.shape
		if data.dtype.kind == 'b':
			var['.dsize'] = 1
		elif data.dtype.kind in ('U', 'S', 'O'):
			var['.dsize'] = 8
		else:
			var['.dsize'] = data.dtype.itemsize*8
		count = np.prod(var['.size'])
		if data.dtype.kind in ('U', 'O'):
			var['.len'] = int(8*count + \
				sum([len(str(x).encode('utf-8')) for x in data.flatten()]))
		else:
			var['.len'] = int(np.ceil(var['.dsize']*count/8))
		if data.dtype.kind in TYPES:
			var['.type'] = TYPES[data.dtype.kind]
		elif data.dtype.kind == 'O':
			if all([type(x) is bytes for x in data.flatten()]):
				var['.type'] = 'str'
			else:
				var['.type'] = 'unicode'
		else:
			continue
		var['.offset'] = offset
		var['.missing'] = bool(isinstance(data, np.ma.MaskedArray) and \
			np.ma.getmask(data.mask) != np.ma.nomask)
		var['.len'] += int(np.ceil(var['.missing']*count/8))
		if data.dtype.kind in ('U', 'S', 'O'):
			var['.endian'] = sys.byteorder
		elif data.dtype.kind == 'b':
			pass
		else:
			var['.endian'] = {
				'<': 'l',
				'>': 'b',
				'=': sys.byteorder[0],
				'|': 'b',
			}[data.dtype.byteorder]
		offset += var['.len']
		meta[name] = var
	meta['.'] = ds.get_meta(d, '.')
	meta_s = json.dumps(meta, cls=JSONEncoder)
	with open(filename, 'wb') as f:
		f.write(meta_s.encode('utf-8') + b'\n')
		for name in ds.get_vars(d):
			var = meta[name]
			if name not in meta:
				continue
			data = ds.get_var(d, name)
			if data.dtype.kind in ('U', 'S', 'O'):
				slen = np.array([len(x) for x in data.flatten()], np.uint64)
				slen.tofile(f)
				for x in data.flatten():
					if data.dtype.kind == 'S':
						f.write(x)
					else:
						f.write(str(x).encode('utf-8'))
			else:
				data2 = np.array(data) if isinstance(data, np.ma.MaskedArray) \
					else data
				if var['.type'] == 'bool':
					data2 = np.packbits(data2)
				data2.tofile(f)
			if var['.missing'] is True:
				mask = np.packbits(data.mask)
				mask.tofile(f)
