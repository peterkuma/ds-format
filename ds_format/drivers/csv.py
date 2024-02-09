import csv
import numpy as np
import ds_format as ds
from ds_format import misc

READ_EXT = ['csv', 'tsv', 'tab']
WRITE_EXT = ['csv', 'tsv', 'tab']

def convert_read(x):
	for f in [int, float]:
		try: return f(x)
		except (ValueError, TypeError): pass
	if x == '':
		return None
	return x

def convert_write(x):
	if x is np.ma.masked:
		return ''
	return x

def read(filename, variables=None, sel=None, full=False, jd=False, opts={}):
	header = None
	ncols = 0
	x = []
	sep = opts.get('sep')
	if sep is None: sep = '\t' if filename.endswith(('tsv', 'tab')) else ','
	with open(filename) as f:
		reader = csv.reader(f, delimiter=sep)
		for row in reader:
			if header is None:
				header = row
				ncols = len(header)
				x = [[] for i in range(ncols)]
				continue
			for j in range(ncols):
				x[j].append(convert_read(row[j]) if len(row) > j else None)
	d = {}
	for j in range(ncols):
		var = header[j]
		ds.var(d, var, x[j])
		meta = {
			'.dims': ['i'],
			'.type': ds.type(d, var),
			'.size': ds.size(d, var),
		}
		if variables is not None and var not in variables:
			del d[var]
			if full:
				ds.meta(d, var, meta)
			continue
		ds.meta(d, var, meta)
	ds.validate(d)
	if sel is not None:
		ds.select(d, sel)
	return d

def write(filename, d, opts={}):
	ds.validate(d)
	header = []
	x = []
	sep = opts.get('sep')
	if sep is None: sep = '\t' if filename.endswith(('tsv', 'tab')) else ','
	for var in ds.vars(d):
		data = ds.var(d, var)
		if data is not None and data.ndim > 1:
			raise ValueError('%s: variable has more than one dimension (not supported in CSV)' % var)
		header.append(var)
		x.append(data)
	ncols = len(x)
	if ncols > 0:
		length = [len(x[i]) for i in range(ncols)]
		if max(length) != min(length):
			raise ValueError('variables have different size (not supported in CSV)')
		nrows = max(length)
	else:
		nrows = 0
	with open(filename, 'w') as f:
		writer = csv.writer(f, delimiter=sep)
		if ncols > 0:
			writer.writerow(header)
		for j in range(nrows):
			writer.writerow([convert_write(x[i][j]) for i in range(ncols)])
