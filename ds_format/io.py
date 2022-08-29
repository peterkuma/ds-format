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
	'''
	title: read
	caption: "Read dataset from a file."
	usage: "`read`(*filename*, *variables*=`None`, *sel*=`None`, *full*=`False`, *jd*=`False`)"
	arguments: {{
		*filename*: "Filename (`str`)."
		*variables*: "Variable names to read (`list` of `str`)."
	}}
	options: {{
		*sel*: "Selector (see **[select](#select)**)."
		*full*: "Read all metadata (`bool`)."
		*jd*: "Convert time variables to Julian dates (see [Aquarius Time](https://github.com/peterkuma/aquarius-time)) (`bool`)."
	}}
	"Supported formats": {{
		DS: `.ds`
		JSON: `.json`
		NetCDF4: "`.nc`, `.nc4`, `.nc3`, `.netcdf`, `.hdf`, `.h5`"
	}}
	returns: "Dataset (`dict`)."
	'''
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
	'''
	title: readdir
	caption: "Read multiple files in a directory."
	usage: "`readdir`(*dirname*, *variables*=`None`, *merge*=`None`, *warnings*=[], ...)"
	arguments: {{
		*dirname*: "Directory name."
	}}
	options: {{
		*variables*: "Variable names to read (`list` of `str`)."
		*merge*: "Dimension name to merge datasets by."
		*warnings*: "Array to be populated with warnings."
		...: "Optional keyword arguments passed to **[read](#read)**."
	}}
	returns: "A list of datasets (`list` of `dict`) if *merge* is `None` or a merged dataset (`dict`) if *merge* is a dimension name."
	'''
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
			m = ds.dims(d)[merge]
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
	'''
	title: write
	usage: "`write`(*filename*, *d*)"
	caption: "Write dataset to a file."
	desc: "The file type is determined from the file extension."
	arguments: {{
		*filename*: "Filename (`str`)."
		*d*: "Dataset (`dict`)."
	}}
	"Supported formats": {{
		NetCDF4: "`.nc`, `.nc4`, `.netcdf`"
		JSON: `.json`
		DS: `.ds`
	}}
	returns: `None`
	'''
	for name, driver in DRIVERS.items():
		for ext in driver.WRITE_EXT:
			end = '.' + ext
			if type(filename) is bytes:
				end = end.encode('utf-8')
			if filename.endswith(end):
				driver.write(filename, d)
				return
	raise ValueError('%s: Unknown file extension' % filename)
