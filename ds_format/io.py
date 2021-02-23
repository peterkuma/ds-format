import os
import traceback as tb
from .drivers import DRIVERS
import ds_format as ds
import numpy as np

def index(dirname, variables=None, warnings=[], **kwargs):
	l = sorted(os.listdir(dirname))
	dd = []
	for name in l:
		filename = os.path.join(dirname, name)
		try: d = ds.read(filename, variables=variables, **kwargs)
		except Exception as e:
			warnings.append((
				'%s: %s' % (filename, e),
				tb.format_exc()
			))
			continue
		d['filename'] = filename
		d['.']['filename'] = {
			'.dims': [],
		}
		dd.append(d)
	return dd

def read(filename, *args, **kwargs):
	if not os.path.exists(filename):
		raise IOError('%s: File does not exist' % filename)
	for name, driver in DRIVERS.items():
		for ext in driver.READ_EXT:
			end = '.' + ext
			if type(filename) is bytes:
				end = end.encode('utf-8')
			if filename.endswith(end):
				d = driver.read(filename, *args, **kwargs)
				return d
	raise IOError('%s: Unknown file format' % filename)

def readdir(dirname, variables=None, merge=None, warnings=[], **kwargs):
	l = sorted(os.listdir(dirname))
	dd = []
	for name in l:
		filename = os.path.join(dirname, name)
		try: d = ds.read(filename, variables=variables, **kwargs)
		except Exception as e:
			warnings.append((
				'%s: %s' % (filename, e),
				tb.format_exc()
			))
			continue
		d['filename'] = filename
		d['.']['filename'] = {
			'.dims': [],
		}
		dd.append(d)
	if merge is None:
		return dd
	else:
		n = 0
		for n, d in enumerate(dd):
			m = ds.get_dims(d)[merge]
			d['n'] = np.full(m, n)
			d['i'] = np.arange(m)
			d['.']['n'] = {
				'.dims': [merge],
			}
			d['.']['i'] = {
				'.dims': [merge],
			}
		d = ds.op.merge(dd, merge, new='n')
		return d

def write(filename, d):
	for name, driver in DRIVERS.items():
		for ext in driver.WRITE_EXT:
			end = '.' + ext
			if type(filename) is bytes:
				end = end.encode('utf-8')
			if filename.endswith(end):
				driver.write(filename, d)
				return
	raise ValueError('%s: Unknown file extension' % filename)
