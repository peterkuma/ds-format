import os
import glob
import traceback as tb
from .drivers import DRIVERS
import ds_format as ds
from ds_format.misc import check
import numpy as np
from concurrent.futures import ProcessPoolExecutor

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
		ds.var(d, 'filename', filename)
		ds.dims(d, 'filename', [])
		dd.append(d)
	return dd

def read(filename, variables=None, sel=None, full=False, jd=False):
	'''
	title: read
	caption: "Read dataset from a file."
	usage: "`read`(*filename*, *variables*=`None`, *sel*=`None`, *full*=`False`, *jd*=`False`)"
	arguments: {{
		*filename*: "Filename (`str`, `bytes` or `os.PathLike`)."
		*variables*: "Variable names to read (`str` or `list` of `str`) or `None` to read all variables."
	}}
	options: {{
		*sel*: "Selector (see **[select](#select)**)."
		*full*: "Read all metadata (`bool`)."
		*jd*: "Convert time variables to Julian dates (see [Aquarius Time](https://github.com/peterkuma/aquarius-time)) (`bool`)."
	}}
	"Supported formats": {{
		CSV/TSV: "`.csv`, `.tsv`, `.tab`"
		DS: `.ds`
		HDF5: "`.h5`, `.hdf5`, `.hdf`"
		JSON: `.json`
		NetCDF4: "`.nc`, `.nc4`, `.nc3`, `.netcdf`"
	}}
	returns: "Dataset (`dict`)."
	examples: {{
		"Read a file `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ print(d.keys())
dict_keys(['.', 'temperature', 'time'])
$ print(d['temperature'])
[16. 18. 21.]
$ d['.']['temperature']
{'long_name': 'temperature', 'units': 'celsius', '.dims': ('time',), '.size': (3,), '.type': 'float64'}"
		"Read a variable `temperature` at an index 0 of the dimension `time` from `dataset.nc`.":
"$ d = ds.read('dataset.nc', 'temperature', sel={'time': 0})
$ d.keys()
dict_keys(['.', 'temperature'])
$ print(d['temperature'])
16.0"
		"Read only the metadata of `dataset.nc`.":
"$ d = ds.read('dataset.nc', [], full=True)
$ d.keys()
dict_keys(['.'])
$ print(d['.'])
{'.': {'title': 'Temperature data'}, 'temperature': {'long_name': 'temperature', 'units': 'celsius', '.dims': ('time',), '.size': (3,), '.type': 'float64'}, 'time': {'long_name': 'time', 'units': 's', '.dims': ('time',), '.size': (3,), '.type': 'int64'}}"
	}}
	'''
	check(filename, 'filename', [str, bytes, os.PathLike])
	check(variables, 'variables', [str, [list, str], [tuple, str], None])
	check(sel, 'sel', [[dict, str], None])
	if isinstance(filename, os.PathLike): filename = filename.__fspath__()
	if not os.path.exists(filename):
		raise IOError('%s: File does not exist' % filename)
	for name, driver in DRIVERS.items():
		for ext in driver.READ_EXT:
			end = '.' + ext
			if isinstance(filename, bytes):
				end = end.encode('utf-8')
			if filename.endswith(end):
				d = driver.read(filename, variables, sel, full, jd)
				return d
	raise IOError('%s: Unknown file format' % filename)

def readdir_worker(args):
	filename, extensions, variables, kwargs = args
	warnings = []
	if not os.path.isfile(filename) or not filename.endswith(extensions):
		return None, warnings
	try: d = ds.read(filename, variables=variables, **kwargs)
	except Exception as e:
		warnings += [(
			'%s: %s' % (filename, e),
			tb.format_exc()
		)]
		return None, warnings
	ds.var(d, 'filename', filename)
	ds.dims(d, 'filename', [])
	return d, warnings

def readdir(dirname, variables=None, merge=None, warnings=[], recursive=False,
	parallel=False, executor=None, njobs=None, **kwargs):
	'''
	title: readdir
	caption: "Read all data files in a directory."
	usage: "`readdir`(*dirname*, *variables*=`None`, *merge*=`None`, *warnings*=[], *recursive*=`False`, *parallel*=`False`, *executor*=`None`, *njobs*=`None`, ...)"
	arguments: {{
		*dirname*: "Directory name (`str`, `bytes` or `os.PathLike`)."
	}}
	desc: "Only files with known extensions are read. Files are read in an alphabetical order. Variable `filename` is added to the output datasets, containing the name of the file. If *merge* is not `None`, variables `i` and `n` are added to the resulting dataset, containing the index within the input dataset and a file index referring to the `filename` variable, respectively. They are defined along the dimension *merge* and are zero-indexed."
	options: {{
		*recursive*: "If true, read the directory recursively (`bool`). Otherwise only files in the top-level directory are read."
		*variables*: "Variable names to read (`str` or `list` of `str`) or `None` to read all variables."
		*merge*: "Dimension name to merge datasets by (`str`) or `None`."
		*warnings*: "A list to be populated with warnings (`list`)."
		*parallel*: "Enable parallel execution."
		*executor*: "`concurrent.futures.Executor` instance or `None` to use a new executor."
		*njobs*: "Number of parallel jobs or `None` to use the number of CPU cores."
		...: "Optional keyword arguments passed to **[read](#read)**."
	}}
	"Supported formats": {{
		CSV/TSV: "`.csv`, `.tsv`, `.tab`"
		DS: `.ds`
		HDF5: "`.h5`, `.hdf5`, `.hdf`"
		JSON: `.json`
		NetCDF4: "`.nc`, `.nc4`, `.nc3`, `.netcdf`"
	}}
	returns: "A list of datasets (`list` of `dict`) if *merge* is `None` or a merged dataset (`dict`) if *merge* is a dimension name."
	examples: {{
		"Read datasets `dataset1.nc` and `dataset2.nc` in the current directory (`.`).":
"$ ds.write('dataset1.nc', { 'time': [1, 2, 3], 'temperature': [16., 18., 21.], '.': {
	'time': { '.dims': ['time'] },
	'temperature': { '.dims': ['time'] },
}})
$ ds.write('dataset2.nc', { 'time': [4, 5, 6], 'temperature': [23., 25., 28.], '.': {
	'time': { '.dims': ['time'] },
	'temperature': { '.dims': ['time'] },
}})
$ dd = ds.readdir('.')
$ for d in dd: print(d['time'])
[1 2 3]
[4 5 6]"
		"Read datasets in the current directory and merge them by a dimension `time`.":
"$ d = ds.readdir('.', merge='time')
$ print(d['time'])
[1 2 3 4 5 6]
$ print(d['temperature'])
[16. 18. 21. 23. 25. 28.]"
	}}
	'''
	check(dirname, 'dirname', [str, bytes, os.PathLike])
	check(variables, 'variables', [str, [list, str], [tuple, str], None])
	check(merge, 'merge', [str, None])
	check(warnings, 'warnings', list)
	if isinstance(dirname, os.PathLike): dirname = dirname.__fspath__()

	pattern = '**' if recursive else '*'
	files = sorted(glob.glob(os.path.join(glob.escape(dirname), pattern),
		recursive=recursive))
	dd = []
	extensions = tuple(['.' + ext
		for driver in DRIVERS.values()
		for ext in driver.READ_EXT
	])
	mapfn = map
	ex = None
	try:
		if parallel:
			if njobs is None: njobs = os.cpu_count()
			ex = ProcessPoolExecutor(njobs) if executor is None else executor
			mapfn = ex.map
		if ex is not None: ex.__enter__()
		res = mapfn(readdir_worker, [
			(filename, extensions, variables, kwargs)
			for filename in files
		])
	except Exception:
		if ex is not None: ex.__exit__()
		raise
	dd = []
	for d, w in res:
		warnings += w
		if d is None:
			continue
		dd += [d]
	if merge is None:
		return dd
	else:
		n = 0
		for n, d in enumerate(dd):
			m = ds.dims(d, size=True)[merge]
			ds.var(d, 'n', np.full(m, n))
			ds.var(d, 'i', np.arange(m))
			ds.dims(d, 'n', [merge])
			ds.dims(d, 'i', [merge])
		d = ds.op.merge(dd, merge, new='n')
		return d

def write(filename, d):
	'''
	title: write
	usage: "`write`(*filename*, *d*)"
	caption: "Write dataset to a file."
	desc: "The file type is determined from the file extension."
	arguments: {{
		*filename*: "Filename (`str`, `bytes` or `os.PathLike`)."
		*d*: "Dataset (`dict`)."
	}}
	"Supported formats": {{
		CSV/TSV: "`.csv`, `.tsv`, `.tab`"
		DS: `.ds`
		HDF5: "`.h5`, `.hdf5`, `.hdf`"
		JSON: `.json`
		NetCDF4: "`.nc`, `.nc4`, `.netcdf`"
	}}
	returns: `None`
	examples: {{
		"Write a dataset to a file `dataset.nc`.":
"$ ds.write('dataset.nc', {
	'time': [1, 2, 3],
	'temperature': [16. 18. 21.],
})"
		"Write a dataset with metadata to a file `dataset.nc`.":
"$ ds.write('dataset.nc', {
	'time': [1, 2, 3],
	'temperature': [16. 18. 21.],
	'.': {
		'.': { 'title': 'Temperature data' },
		'time': { '.dims': ['time'] },
		'temperature': { '.dims': ['time'], 'units': 'degree_celsius' },
	}
})"
	}}
	'''
	check(filename, 'filename', [str, bytes, os.PathLike])
	check(d, 'd', dict)
	if isinstance(filename, os.PathLike): filename = filename.__fspath__()
	for driver in DRIVERS.values():
		for ext in driver.WRITE_EXT:
			end = '.' + ext
			if isinstance(filename, bytes):
				end = end.encode('utf-8')
			if filename.endswith(end):
				driver.write(filename, d)
				return
	raise ValueError('%s: Unknown file extension' % filename)
