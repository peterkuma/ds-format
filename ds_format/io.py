import os
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
			warnings.append(e)
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
			if filename.endswith('.' + ext):
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
			warnings.append('%s: %s' % (filename, e))
			continue
		d['filename'] = filename
		d['.']['filename'] = {
			'.dims': [],
		}
		dd.append(d)
	if merge is None:
		return dd
	else:
		d = ds.op.merge(dd, merge)
		return d

def write(filename, d):
	for name, driver in DRIVERS.items():
		for ext in driver.WRITE_EXT:
			if filename.endswith('.' + ext):
				driver.write(filename, d)	
				return
	raise ValueError('%s: Unknown file extension' % filename)
