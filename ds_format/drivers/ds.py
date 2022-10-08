import sys
import json
from copy import copy
import numpy as np
import ds_format as ds
from ds_format import misc

VERSION = '1.0'

READ_EXT = ['ds']
WRITE_EXT = ['ds']

TYPE_SIZE = {
	'int8': 8,
	'int16': 16,
	'int32': 32,
	'int64': 64,
	'uint8': 8,
	'uint16': 16,
	'uint32': 32,
	'uint64': 64,
	'float32': 32,
	'float64': 64,
	'bool': 1,
	'str': 8,
	'unicode': 8,
	None: 0,
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
		version_s = f.readline()
		if not version_s.startswith(b'ds-'):
			raise IOError('invalid format version string')
		version = version_s[3:-1]
		if version != b'1.0':
			raise IOError('unsupported format version')
		header = f.readline()
		meta_s = header.decode('utf-8')
		meta = json.loads(meta_s)
		d['.'] = meta
		data_offset = len(version_s) + len(header)
		if variables is not None and not full:
			meta = {k: v for k, v in meta.items() if k in variables}
		for name in meta.keys():
			if name.startswith('.') or \
			   variables is not None and name not in variables:
				continue
			var = meta[name]
			if not ('.offset' in var and \
			   		'.type' in var and \
			   		'.len' in var and \
			   		'.size' in var and \
					'.endian' in var):
				continue
			dt = misc.type_to_dtype(var['.type'])
			if dt is None:
				continue
			byteorder = {
				'l': '<',
				'b': '>',
			}[var['.endian']]
			count = 0 if var['.size'] is None else int(np.prod(var['.size']))
			mask_len = int(np.ceil(count/8)) if var['.missing'] else 0

			if var['.missing'] and count > 0:
				f.seek(data_offset + var['.offset'])
				mask = np.fromfile(f, 'uint8', count=mask_len)
				mask = np.unpackbits(mask)[:count].astype(bool)
				mask = mask.reshape(var['.size'])
				count2 = np.sum(~mask)
			else:
				count2 = count

			if count == 0:
				data = None
			else:
				var_len = int(count2*TYPE_SIZE[var['.type']]/8)
				f.seek(data_offset + var['.offset'] + mask_len)
				if var['.type'] == 'bool':
					data = np.fromfile(f, 'uint8', count=var_len)
					data = np.unpackbits(data)[:count2]
					data = data.astype(bool)
				elif var['.type'] in ('str', 'unicode'):
					dt_slen = np.dtype('uint64').newbyteorder(byteorder)
					slen = np.fromfile(f, dt_slen, count=count2)
					data = []
					for slen1 in slen:
						if var['.type'] == 'str':
							data += [f.read(slen1)]
						else:
							data += [f.read(slen1).decode('utf-8')]
					data = np.array(data, 'O')
				else:
					dt = dt.newbyteorder(byteorder)
					data = np.fromfile(f, dt, count=count2)

				if var['.missing']:
					data2 = np.zeros(var['.size'], dtype=dt)
					data2[~mask] = data
					data = np.ma.array(data2, mask=mask)
				else:
					data = data.reshape(var['.size'])

				if var['.size'] == []:
					data = data[()]

			if sel is not None:
				#s = ds.misc.sel_slice(sel, dims)
				#mask = mask[s]
				dims = ds.dims(d, name)
				s = ds.misc.sel_slice(sel, dims)
				dims = ds.misc.sel_dims(sel, dims)
				var['.dims'] = dims
				data = data[s]
			d[name] = data
	if jd:
		for var in ds.vars(d):
			misc.process_time_var(d, var)
	return d

def write(filename, d):
	ds.validate(d)
	offset = 0
	meta = {}
	for name in ds.vars(d):
		var = copy(ds.meta(d, name))
		data = ds.var(d, name)
		dtype = None if data is None else data.dtype
		var['.size'] = None if data is None else list(data.shape)
		count = 0 if var['.size'] is None else np.prod(var['.size'])
		var['.offset'] = offset
		var['.len'] = 0
		var['.type'] = var.get('.type') if dtype is None else \
			misc.dtype_to_type(dtype, data)
		var['.missing'] = bool(isinstance(data, np.ma.MaskedArray) and \
			np.ma.is_masked(data))
		if var['.missing']:
			var['.len'] += int(np.ceil(count/8))
		count2 = np.sum(~data.mask) if var['.missing'] else count
		if dtype is not None and dtype.kind in ('U', 'O'):
			var['.len'] += int(8*count2 + \
				sum([len(str(x).encode('utf-8')) for x in data.flatten()]))
		elif dtype is not None and dtype.kind == 'S':
			var['.len'] += int(8*count2 + \
				sum([len(x) for x in data.flatten()]))
		else:
			var['.len'] += int(np.ceil(TYPE_SIZE[var['.type']]*count2/8))
		if dtype is not None and dtype.kind in ('U', 'S', 'O'):
			var['.endian'] = sys.byteorder[0]
		elif var['.type'] == 'bool':
			pass
		elif dtype is not None:
			var['.endian'] = {
				'<': 'l',
				'>': 'b',
				'=': sys.byteorder[0],
				'|': 'b',
			}[dtype.byteorder]
		offset += var['.len']
		meta[ds.escape(name)] = var
	meta['.'] = ds.meta(d, '.')
	meta_s = json.dumps(meta, cls=JSONEncoder)
	with open(filename, 'wb') as f:
		header = \
			b'ds-%b\n' % VERSION.encode('utf-8') + \
			meta_s.encode('utf-8') + \
			b'\n'
		f.write(header)
		for name in ds.vars(d):
			if ds.escape(name) not in meta:
				continue
			var = meta[ds.escape(name)]
			data = ds.var(d, name)
			if data is None:
				continue
			data = data.flatten()
			if var['.missing'] is True:
				mask = np.packbits(data.mask)
				mask.tofile(f)
			data2 = np.array(data) if not var['.missing'] else \
				np.array(data)[~data.mask]
			if var['.type'] in ['str', 'unicode']:
				data3 = [
					x.encode('utf-8') if type(x) in [str, np.str_] else x
					for x in data2
				]
				slen = np.array([len(x) for x in data3], np.uint64)
				slen.tofile(f)
				for x in data3:
					f.write(x)
			else:
				if var['.type'] == 'bool':
					data2 = np.packbits(data2)
				data2.tofile(f)
