import types
import fnmatch
import numpy as np
import copy as copy_
import datetime as dt
from warnings import warn, catch_warnings
from collections.abc import Mapping, Iterable
import ds_format as ds
from ds_format.misc import check
from . import misc

#
# Private variables.
#

ALLOWED_TYPES = [
	'float32',
	'float64',
	'int8',
	'int16',
	'int32',
	'int64',
	'uint8',
	'uint16',
	'uint32',
	'uint64',
	'bool',
	'str',
	'unicode',
]

#
# Private functions.
#

def select_var(d, var, sel):
	var_e = ds.escape(var)
	var_dims = ds.dims(d, var)
	d['.'][var_e]['.dims'] = var_dims
	for k, v in sel.items():
		if isinstance(v, Mapping):
			if len(sel) > 1: raise ValueError('invalid selector')
			newdim = k
			dims = v.keys()
			idxs = v.values()
			selector = tuple([
				idxs[dims.index(var_dim)] if var_dim in dims else slice(None)
				for var_dim in var_dims
			])
			data = ds.var(d, var)
			ds.var(d, var, data[selector])
			for dim in dims:
				if dim in var_dims:
					var_dims.remove(dim)
			d['.'][var_e]['.dims'].append(newdim)
		else:
			dim, idxs = k, v
			idxs = np.array(idxs) if isinstance(idxs, (list, tuple)) else idxs
			if isinstance(idxs, np.ndarray) and idxs.dtype == np.bool_:
				idxs = np.nonzero(idxs)[0]
			if dim in var_dims:
				i = var_dims.index(dim)
				data = ds.var(d, var)
				ds.var(d, var, np.take(data, idxs, axis=i))
				if not isinstance(idxs, np.ndarray):
					var_dims.remove(dim)

def is_hidden(x):
	return isinstance(x, bytes) and x.startswith(b'.') or \
		isinstance(x, str) and x.startswith('.')

def filter_hidden(x):
	if isinstance(x, Mapping):
		return {k: v for k, v in x.items() if not is_hidden(k)}
	if isinstance(x, Iterable):
		return [k for k in x if not is_hidden(k)]
	return x

def gen_dims(d, var):
	data = ds.var(d, var)
	size = ds.size(d, var)
	return [] if size is None else \
		[var + ('_%d' % i) for i in range(1, len(size) + 1)]

def parse_time(t):
	formats = [
		'%Y-%m-%d %H:%M:%S.%f',
		'%Y-%m-%d %H:%M:%S',
		'%Y-%m-%dT%H:%M:%SZ',
	]
	for f in formats:
		try: return dt.datetime.strptime(t, f)
		except: pass
	return None

def time_dt(time):
	return [parse_time(t) for t in time]

def merge_var(dd, var, dim, jd=True):
	for d in dd:
		x = ds.var(d, var)
		if x is None:
			continue
		dims0 = ds.dims(d, var)
		size0 = ds.size(d, var)
		type_ = ds.type(d, var)
		dt = misc.type_to_dtype(type_)
		try: k = dims0.index(dim)
		except ValueError: k = None
		break
	else:
		return None, None

	convert_time = False
	if jd:
		units = None
		for d in dd:
			attrs = ds.attrs(d, var)
			u = attrs.get('units')
			if units is None: units = u
			if u != units:
				convert_time = True
				break

	if k is None: # New dimension.
		n = len(dd)
		dims = [dim] + dims0
		size = [n] + size0
	else: # Existing dimension.
		n = np.sum([ds.dim(d, dim) for d in dd])
		dims = dims0
		size = copy_.deepcopy(size0)
		size[k] = n

	x = np.ma.array(np.zeros(size, dt), mask=np.ones(size, bool))
	i = 0
	meta = {}
	for d in dd:
		if convert_time:
			d2 = {}
			ds.var(d2, var, ds.var(d, var))
			ds.meta(d2, var, ds.meta(d, var))
			misc.process_time_var(d2, var)
			d = d2
		x1 = ds.var(d, var)
		n1 = 1 if k is None else ds.dim(d, dim)
		if x1 is None:
			i += n1
			continue
		dims1 = ds.dims(d, var)
		size1 = ds.size(d, var)
		if dims1 != dims0:
			raise ValueError('merge: incompatible dimensions in variable "%s"' % var)
		if len(size0) != len(size1) or \
		   not all(i == k or size1[i] == size0[i] for i in range(len(size0))):
			raise ValueError('merge: incompatible size in variable "%s"' % var)
		if k is None:
			sel = [i] + [slice(None) for j in range(len(size0))]
		else:
			sel = [slice(i, i + n1) if j == k else slice(None) \
				for j in range(len(size))]
		x[tuple(sel)] = x1
		meta.update(ds.meta(d, var))
		i += n1
	meta['.dims'] = dims
	return x, meta

def copy(d):
	d2 = {}
	for var in ds.vars(d):
		data = ds.var(d, var)
		ds.var(d2, var, data)
	meta = ds.meta(d)
	ds.meta(d2, None, copy_.deepcopy(meta))
	return d2

def normalize_var(data):
	if isinstance(data, (list, tuple)):
		with catch_warnings(action='ignore'):
			data = np.ma.asarray(data)
		data = np.ma.masked_equal(data, None)
		mask = data.mask.copy()
		if np.ma.is_masked(data):
			data[mask] = 0
			tmp = data.flatten().tolist()
			data = np.ma.array(tmp, mask=mask)
		else:
			data = np.asarray(data)
	if isinstance(data, (int, float, bool, str, bytes)):
		data = np.array(data)[()]
	if data is None or \
		isinstance(data, (np.ndarray, np.generic)) and ( \
		data.dtype.name in ALLOWED_TYPES or \
		data.dtype.name.startswith(('str', 'bytes')) or \
		(data.dtype.name == 'object' and \
		all([isinstance(x, (str, bytes)) or x is None for x in data.flatten()]))):
		if isinstance(data, np.ndarray) and data.ndim == 0:
			return data[()]
		else:
			return data
	else:
		raise ValueError('invalid data type')

#
# Public functions.
#

def attr(d, attr, *value, var=None):
	'''
	title: attr
	caption: "Get or set a dataset or variable attribute."
	usage: "`attr`(*d*, *attr*, \**value*, *var*=`None`)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*attr*: "Attribute name (`str`)."
		*value*: "Attribute value. If supplied, set the attribute value, otherwise get the attribute value."
	}}
	options: {{
		*var*: "Variable name (`str`) to get or set a variable attribute, or `None` to get or set a dataset attribute."
	}}
	returns: "Attribute value if *value* is not set, otherwise `None`."
	examples: {{
		"Get an attribute `long_name` of a variable `temperature` in `dataset.nc`.":
"$ d = ds.read('dataset.nc')
ds.attr(d, 'long_name', var='temperature')
'temperature'"
		"Get a dataset attribute `title` of `dataset.nc`.":
"$ ds.attr(d, 'title')
'Temperature data'"
		"Set an attribute `units` of a variable `temperature` to `K`.":
"$ ds.attr(d, 'units', 'K', var='temperature')
$ ds.attr(d, 'units', var='temperature')
'K'"
	}}
	'''
	check(d, 'd', dict)
	check(attr, 'attr', str)
	check(var, 'var', [str, None])
	if len(value) == 0:
		if require(d, 'attr', attr, var):
			attrs = ds.attrs(d, var)
			return attrs[attr]
		else:
			return None
	elif len(value) == 1:
		meta = ds.meta(d, '' if var is None else var, create=True)
		meta[ds.escape(attr)] = value[0]
	else:
		raise TypeError('only one value argument is expected')

def attrs(d, var=None, *value):
	'''
	title: attrs
	caption: "Get or set variable or dataset attributes."
	usage: "`attrs`(*d*, *var*=`None`, \**value*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*value*: "Attributes to set (`dict`). If supplied, set attributes to *value*, otherwise get attributes."
	}}
	options: {{
		*var*: "Variable name (`str`) or `None` to get dataset attributes."
	}}
	returns: "Attributes (`dict`)."
	examples: {{
		"Get attributes of a variable `temperature` in a dataset `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}"
		"Get dataset attributes.":
"$ ds.attrs(d)
{'title': 'Temperature data'}"
		"Set attributes of a variable `temperature`.":
"$ ds.attrs(d, 'temperature', {'long_name': 'new temperature', 'units': 'K'})
$ ds.attrs(d, 'temperature')
{'long_name': 'new temperature', 'units': 'K'}"
	}}
	'''
	check(d, 'd', dict)
	check(var, 'var', [str, None])
	if len(value) == 0:
		meta = ds.meta(d, '' if var is None else var)
		return {ds.unescape(k): v for k, v in filter_hidden(meta).items()}
	elif len(value) == 1:
		check(value[0], 'value', [[dict, str]])
		for k, v in value[0].items():
			ds.attr(d, k, v, var=var)
	else:
		raise TypeError('only one value argument is expected')

get_attrs = attrs

def dim(d, dim, full=False):
	'''
	title: dim
	caption: "Get a dimension size."
	usage: "`dim`(*d*, *dim*, *full*=`None`)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*dim*: "Dimension name (`str`)."
	}}
	options: {{
		*full*: "Return dimension size also for a dimension for which no variable data are defined, i.e. it is only defined in dataset metadata."
	}}
	returns: "Dimension size or 0 if the dimension does not exist (`int`)."
	examples: {{
		"Get the size of a dimension `time` in `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.dim(d, 'time')
3"
		"Get the size of a dimension `time` in `dataset.nc` without reading data.":
"$ d = ds.read('dataset.nc', full=True)
$ ds.dim(d, 'time', full=True)
3"
	}}
	'''
	check(d, 'd', dict)
	check(dim, 'dim', str)
	if require(d, 'dim', dim):
		return dims(d, full=full, size=True)[dim]
	return 0

def dims(d, var=None, *value, full=False, size=False):
	'''
	title: dims
	aliases: { get_dims }
	usage: {
		"`dims`(*d*, *var*=`None`, \**value*, *full*=`False`, *size*=`False`)"
		"`get_dims`(*d*, *var*=`None`, *full*=`False`, *size*=`False`)"
	}
	caption: "Get dataset or variable dimensions or set variable dimensions."
	desc: "The function `get_dims` (deprecated) is the same as `dims`, but assumes that *size* is True if *var* is None and does not allow setting of dimensions."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*value*: "A list of dimensions (`list` of `str`) or `None`. If supplied, set variable dimensions, otherwise get dataset or variable dimensions. If `None`, remove variable dimensions (will be set to autogenerated names on write). If supplied, *var* must not be None."
	}}
	options: {{
		*var*: "Variable name (`str`) or `None` to get dimensions for."
		*full*: "Get variable dimensions even if the variable is only defined in the metadata (`bool`)."
		*size*: "Return a dictionary containing dimension sizes instead of a list."
	}}
	returns: "If *size* is False, a list of dataset or variable dimension names (`list` of `str`). If *size* is True, a dictionary of dataset or variable dimension names and sizes (`dict`), where a key is a dimension name (`str`) and the value is the dimension size (`int`). The order of keys in the dictionary is not guaranteed. Dataset dimensions are the dimensions of all variables together."
	examples: {{
		"Get dimensions of a dataset `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.dims(d)
['time']"
		"Get dimension sizes.":
"$ ds.dims(d, size=True)
{'time': 3}"
		"Get dimensions of a variable `temperature`.":
"$ ds.dims(d, 'temperature')
['time']"
	}}
	'''
	check(d, 'd', dict)
	check(var, 'var', [str, None])
	if len(value) == 0:
		if var is None:
			if size:
				dims = {}
				for name in ds.vars(d, full):
					var_dims = ds.dims(d, name, size=True)
					for k, v in var_dims.items():
						dims[k] = v
				return dims
			else:
				dims = set()
				for name in ds.vars(d, full):
					var_dims = ds.dims(d, name)
					dims |= set(var_dims)
				return sorted(list(dims))
		else:
			meta = ds.meta(d, var)
			if '.dims' in meta:
				var_dims = meta['.dims']
			else:
				var_dims = gen_dims(d, var)
			if size:
				with ds.with_mode('soft'):
					data = ds.var(d, var)
				var_size = meta.get('.size')
				dims = {}
				for i, dim in enumerate(var_dims):
					if data is not None:
						dims[dim] = data.shape[i]
					elif var_size is not None:
						dims[dim] = var_size[i]
					else:
						dims[dim] = None
				return dims
			else:
				if isinstance(var_dims, list):
					return var_dims
				elif isinstance(var_dims, tuple):
					return list(var_dims)
				else:
					return [var_dims]
	elif len(value) == 1:
		check(value[0], 'value', [[list, str], [tuple, str]])
		if var is None:
			raise TypeError('var must be defined')
		meta = ds.meta(d, var, create=True)
		if value[0] is None:
			if '.dims' in meta:
				del meta['.dims']
		else:
			meta['.dims'] = value[0]
	else:
		raise TypeError('only one value argument is expected')

dims.aliases = ['get_dims']

def get_dims(d, var=None, full=False, size=False):
	if var is None:
		size = True
	return dims(d, var, full=full, size=size)

def find(d, what, name, var=None):
	'''
	title: find
	caption: "Find a variable, dimension or attribute matching a glob pattern in a dataset."
	usage: "`find`(*d*, *what*, *name*, *var*=`None`)"
	desc: "If more than one name matches the pattern, raises `ValueError`."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*what*: "Type of item to find (`str`). One of: \\"var\\" (variable), \\"dim\\" (dimension), \\"attr\\" (attribute)."
		*name*: "[Glob pattern](https://docs.python.org/3/library/fnmatch.html) matching a variable, dimension or attribute name (`str`)."
	}}
	options: {{
		*var*: "Variable name (`str`) or `None`. Applies only if *what* is \\"attr\\". If not `none`, *name* is a variable attribute name, otherwise it is a dataset attribute name."
	}}
	returns: "A variable, dimension or attribute name matching the pattern, or *name* if no matching name is found (`str`)."
	examples: {{
		"Find a variable matching the glob pattern `temp*` in a dataset `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.find(d, 'var', 'temp*')
'temperature'"
	}}
	'''
	check(d, 'd', dict)
	check(what, 'what', str)
	check(name, 'name', str)
	check(var, 'var', [str, None])
	names = findall(d, what, name, var)
	desc = {'var': 'variable', 'attr': 'attribute', 'dim': 'dimension'}[what]
	if len(names) > 1:
		raise ValueError('more than one %s is matching the pattern "%s"' % (desc, name))
	elif len(names) == 0:
		#raise ValueError('%s: %s not found' % (name, desc))
		return name
	return names[0]

def findall(d, what, name, var=None):
	'''
	title: findall
	caption: "Find variables, dimensions or attributes matching a glob pattern in a dataset."
	usage: "`findall`(*d*, *what*, *name*, *var*=`None`)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*what*: "Type of item to find (`str`). One of: \\"var\\" (variable), \\"dim\\" (dimension), \\"attr\\" (attribute)."
		*name*: "[Glob pattern](https://docs.python.org/3/library/fnmatch.html) matching a variable, dimension or attribute name (`str`)."
	}}
	options: {{
		*var*: "Variable name (`str`) or `None`. Applies only if *what* is \\"attr\\". If not `none`, *name* is a variable attribute name, otherwise it is a dataset attribute name."
	}}
	returns: "A list of variables, dimensions or attributes matching the pattern, or [*name*] if no matching names are found (`list` of `str`)."
	examples: {{
		"Find all variables matching the glob pattern `t*` in a dataset `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.findall(d, 'var', 't*')
['temperature', 'time']"
	}}
	'''
	check(d, 'd', dict)
	check(what, 'what', str)
	check(name, 'name', str)
	check(var, 'var', [str, None])
	if what == 'var':
		names = ds.vars(d, full=True)
	elif what == 'attr':
		names = ds.attrs(d, var)
	elif what == 'dim':
		names = ds.dims(d, var, full=True)
	else:
		raise ValueError('invalid value of the what argument "%s"' % what)
	res = fnmatch.filter(names, name)
	return [name] if len(res) == 0 else res

def group_by(d, dim, group, func):
	'''
	title: group_by
	caption: "Group values along a dimension."
	usage: "`group_by`(*d*, *dim*, *group*, *func*)"
	desc: "Each variable with a given dimension *dim* is split by *group* into subsets. Each subset is replaced with a value computed by *func*."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*dim*: "Dimension to group along (`str`)."
		*group*: "Groups (`ndarray` or `list`). Array of the same length as the dimension."
		*func*: "Group function (`function`). *func*(*y*, axis=*i*) is called for each subset *y*, where *i* is the index of the dimension."
	}}
	returns: `None`
	examples: {{
		"Calculate mean along a dimension `time` for a group where time <= 2 and a group where time > 2.":
"$ d = {
	'time': np.array([1., 2., 3., 4.]),
	'temperature': np.array([1., 3., 4., 6.]),
	'.': {
		'time': { '.dims': ['time'] },
		'temperature': { '.dims': ['time'] },
	}
}
$ ds.group_by(d, 'time', d['time'] > 2,  np.mean)
$ print(d['time'])
[1.5 3.5]
$ print(d['temperature'])
[1.5 3.5]"
	}}
	'''
	check(d, 'd', dict)
	check(dim, 'dim', str)
	check(group, 'group', [np.ndarray, list, tuple])
	check(func, 'func', types.FunctionType)
	groups = sorted(list(set(group)))
	vars_ = ds.vars(d)
	n = len(groups)
	for var in vars_:
		dims = ds.dims(d, var)
		try:
			i = dims.index(dim)
		except ValueError:
			continue
		data = ds.var(d, var)
		if data is None:
			continue
		size = list(data.shape)
		size[i] = n
		x = np.empty(size, data.dtype)
		for j, g in enumerate(groups):
			mask = group == g
			slice_x = misc.sel_slice({dim: j}, dims)
			slice_y = misc.sel_slice({dim: mask}, dims)
			y = data[slice_y]
			x[slice_x] = func(y, axis=i)
		ds.var(d, var, x)

def merge(dd, dim, new=None, variables=None, jd=True):
	'''
	title: merge
	caption: "Merge datasets along a dimension."
	usage: "`merge`(*dd*, *dim*, *new*=`None`, *variables*=`None`, *jd*=`True`)"
	desc: "Merge datasets along a dimension *dim*. If the dimension is not defined in the dataset, merge along a new dimension *dim*. If *new* is None and *dim* is not new, variables without the dimension *dim* are set with the first occurrence of the variable. If *new* is not None and *dim* is not new, variables without the dimension *dim* are merged along a new dimension *new*. If *variables* is not None, only those variables are merged along a new dimension, and other variables are set to the first occurrence of the variable. Variables which are merged along a new dimension and are not present in all datasets have their subsets corresponding to the datasets where they are missing filled with missing values. Dataset and variable metadata are merged sequentially from all datasets, with metadata from later datasets overriding metadata from the former ones. When merging time variables whose units are not equal and *jd* is `True`, they are first converted to Julian date and then merged."
	arguments: {{
		*dd*: "Datasets (`list`)."
		*dim*: "Name of a dimension to merge along (`str`)."
	}}
	options: {{
		*new*: "Name of a new dimension (`str`) or `None`."
		*variables*: "Variables to merge along a new dimension (`list`) or `None` for all variables."
		*jd*: "Convert time to Julian date when merging time variables with unequal units (`bool`)."
	}}
	returns: "A dataset (`dict`)."
	examples: {{
		"Merge datasets `d1` and `d2` along a dimension `time`.":
"$ d1 = {'time': [1, 2, 3], 'temperature': [16., 18., 21.], '.': {
	'time': { '.dims': ['time'] },
	'temperature': { '.dims': ['time'] },
}}
$ d2 = { 'time': [4, 5, 6], 'temperature': [23., 25., 28.], '.': {
	'time': { '.dims': ['time'] },
	'temperature': { '.dims': ['time'] },
}}
$ d = ds.merge([d1, d2], 'time')
$ print(d['time'])
[1 2 3 4 5 6]
$ print(d['temperature'])
[16. 18. 21. 23. 25. 28.]"
	}}
	'''
	check(dd, 'dd', [[list, dict], [tuple, dict]])
	check(dim, 'dim', str)
	check(new, 'new', [str, None])
	check(variables, 'variables', [[list, str], [tuple, str], None])
	check(jd, 'jd', bool)
	dx = {'.': {'.': {}}}
	vars_ = sorted(list(set([x for d in dd for x in ds.vars(d)])))
	dims = [k for d in dd for k in ds.dims(d)]
	is_new = dim not in dims
	for var in vars_:
		var_dims = None
		for d in dd:
			if var in ds.vars(d):
				var_dims = ds.dims(d, var)
				break
		if is_new and (variables is None or var in variables) or \
		   dim in var_dims:
			x, meta = merge_var(dd, var, dim, jd=jd)
		elif new is not None and (variables is None or var in variables):
			x, meta = merge_var(dd, var, new, jd=jd)
		else:
			x, meta = ds.var(dd[0], var), ds.meta(dd[0], var)
		ds.var(dx, var, x)
		ds.meta(dx, var, meta)
	for d in dd:
		meta = ds.meta(d, '')
		dx['.']['.'].update(meta)
	return dx

def meta(d, var=None, *value, create=False):
	'''
	title: meta
	aliases: { get_meta }
	caption: "Get or set dataset or variable metadata."
	usage: "`meta`(*d*, *var*=`None`, \**value*, *create*=`False`)"
	arguments: {{
		*d*: "Dataset (`dict`)."
	}}
	options: {{
		*var*: "Variable name (`str`), or `None` to get dataset metadata, or an empty string to get dataset attributes."
		*value*: "Metadata to set (`dict`) or `None` to get metadata."
		*create*: "Create (modifiable/bound) metadata dictionary in the dataset if not defined (`bool`). If `False`, the returned dictionary is an empty unbound dictionary if it is not already present in the dataset."
	}}
	returns: "Metadata (`dict`)."
	examples: {{
		"Get metadata of a dataset `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ print(ds.meta(d))
{'.': {'title': 'Temperature data'}, 'temperature': {'long_name': 'temperature', 'units': 'celsius', '.dims': ('time',), '.size': (3,), '.type': 'float64'}, 'time': {'long_name': 'time', 'units': 's', '.dims': ('time',), '.size': (3,), '.type': 'int64'}}"
		"Get metadata of a variable `temperature`.":
"$ ds.meta(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius', '.dims': ('time',), '.size': (3,), '.type': 'float64'}"
		"Set metadata of a variable `temperature`.":
"$ ds.meta(d, 'temperature', { '.dims': ['new_time'], 'long_name': 'new temperature', 'units': 'K'})
$ ds.meta(d, 'temperature')
ds.meta(d, 'temperature', { '.dims': ['new_time'], 'long_name': 'new temperature', 'units': 'K'})"
	}}
	'''
	check(d, 'd', dict)
	check(var, 'var', [str, None])
	var_e = ds.escape(var)

	if len(value) == 0:
		if var is None:
			if '.' in d:
				return d['.']
			if create:
				d['.'] = {}
				return d['.']
			return {}
		elif var == '':
			meta = ds.meta(d, create=create)
			if '.' in meta:
				return meta['.']
			if create:
				meta['.'] = {}
				return meta['.']
			return {}
		else:
			meta = ds.meta(d, create=create)
			if var_e in meta:
				return meta[var_e]
			if create:
				meta[var_e] = {}
				return meta[var_e]
			require(d, 'var', var, full=True)
			return {}
	elif len(value) == 1:
		check(value[0], 'value', [dict, str])
		if var is None:
			d['.'] = value[0]
		else:
			ds_meta = ds.meta(d, create=True)
			ds_meta[var_e] = value[0]
	else:
		raise TypeError('only one value argument is expected')

meta.aliases = ['get_meta']
get_meta = meta

def rename(d, old, new):
	'''
	title: rename
	caption: "Rename a variable."
	usage: "`rename`(*d*, *old*, *new*)"
	desc: "Any dimension with the same name is also renamed."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*old*: "Old variable name (`str`)."
		*new*: "New variable name (`str`) or `None` to remove the variable."
	}}
	returns: `None`
	examples: {{
		"Rename a variable `temperature` to `new_temperature` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.vars(d)
['temperature', 'time']
$ ds.rename(d, 'temperature', 'new_temperature')
$ ds.vars(d)
['new_temperature', 'time']"
	}}
	'''
	check(d, 'd', dict)
	check(old, 'old', str)
	check(new, 'new', [str, None])
	return rename_m(d, {old: new})

def rename_attr(d, old, new, var=None):
	'''
	title: rename_attr
	caption: "Rename a dataset or variable attribute."
	usage: "`rename_attr`(*d*, *old*, *new*, *var*=`None`)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*old*: "Old attribute name (`str`)."
		*new*: "New attribute name (`str`)."
	}}
	options: {{
		*var*: "Variable name (`str`) to rename a variable attribute or `None` to rename a dataset attribute."
	}}
	returns: `None`
	examples: {{
		"Rename an attribute `units` of a variable `temperature` to `new_units` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}
$ ds.rename_attr(d, 'units', 'new_units', var='temperature')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'new_units': 'celsius'}"
		"Rename a dataset attribute `title` to `new_title`.":
"$ ds.attrs(d)
{'title': 'Temperature data'}
$ ds.rename_attr(d, 'title', 'new_title')
$ ds.attrs(d)
{'new_title': 'Temperature data'}"
	}}
	'''
	check(d, 'd', dict)
	check(old, 'old', str)
	check(new, 'new', [str, None])
	check(var, 'var', [str, None])
	return rename_attr_m(d, {old: new}, var)

def rename_attr_m(d, mapping, var=None):
	'''
	title: rename_attr_m
	caption: "Rename one or more dataset or variable attributes."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*mapping*: "A dictionary where the key is an old attribute name (`str`) and the value is a new attribute name (`str`) or `None` to remove the attribute. Swapping of atrributes is also supported."
	}}
	options: {{
		*var*: "Variable name (`str`) to rename a variable attribute or `None` to rename a dataset attribute."
	}}
	returns: `None`
	examples: {{
		"Rename an attribute `long_name` to `new_long_name` and `units` to `new_units` of a variable `temperature` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}
$ ds.rename_attr_m(d, {'long_name': 'new_long_name', 'units': 'new_units'}, var='temperature')
$ ds.attrs(d, 'temperature')
{'new_long_name': 'temperature', 'new_units': 'celsius'}"
		"Rename a dataset attribute `title` to `new_title`.":
"$ ds.attrs(d)
{'title': 'Temperature data'}
$ ds.rename_attr_m(d, {'title': 'new_title'})
$ ds.attrs(d)
{'new_title': 'Temperature data'}"
	}}
	'''
	check(d, 'd', dict)
	check(mapping, 'mapping', dict, str, [str, None])
	tmp = {}
	for old in mapping.keys():
		if not require(d, 'attr', old, var):
			continue
		tmp[old] = ds.attr(d, old, var=var)
		ds.rm_attr(d, old, var)
	for old in tmp.keys():
		new = mapping[old]
		if new is None:
			continue
		ds.attr(d, new, tmp[old], var=var)

def rename_dim(d, old, new):
	'''
	title: rename_dim
	caption: "Rename a dimension."
	usage: "`rename_dim`(*d*, *old*, *new*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*old*: "Old dimension name (`str`)."
		*new*: "New dimension name (`str`)."
	}}
	returns: `None`
	examples: {{
		"Rename a dimension `time` to `new_time` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.dims(d)
['time']
$ ds.rename_dim(d, 'time', 'new_time')
$ ds.dims(d)
['new_time']"
	}}
	'''
	check(d, 'd', dict)
	check(old, 'old', str)
	check(new, 'new', str)
	return rename_dim_m(d, {old: new})

def rename_dim_m(d, mapping):
	'''
	title: rename_dim_m
	caption: "Rename one or more dimensions."
	usage: "`rename_dim_m`(*d*, *mapping*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*mapping*: "A dictionary where the key is an old dimension name (`str`) and the value is a new dimension name (`str`). Swapping of dimensions is also supported."
	}}
	returns: `None`
	examples: {{
		"Rename a dimension `time` to `new_time` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.dims(d)
['time']
$ ds.rename_dim_m(d, {'time': 'new_time'})
$ ds.dims(d)
['new_time']"
	}}
	'''
	check(d, 'd', dict)
	check(mapping, 'mapping', dict, str, str)
	tmp = {}
	for old in mapping.keys():
		for var in ds.vars(d, full=True):
			dims = ds.dims(d, var)
			if old not in dims:
				continue
			tmp[var] = dims
	for old, new in mapping.items():
		for var in ds.vars(d, full=True):
			if var not in tmp:
				continue
			dims = ds.dims(d, var)
			for i, dim in enumerate(tmp[var]):
				if dim == old:
					dims[i] = new
			ds.dims(d, var, dims)

def rename_m(d, mapping):
	'''
	title: rename_m
	caption: "Rename one or more variables."
	usage: "`rename_m`(*d*, *mapping*)"
	desc: "Any dimension with the same name is also renamed."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*mapping*: "A dictionary where the key is an old variable name (`str`) and the value is a new variable name (`str`) or `None` to remove the variable. Swapping of variables is also supported."
	}}
	returns: `None`
	examples: {{
		"Rename a variable `time` to `new_time` and `temperature` to `new_temperature` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.vars(d)
['temperature', 'time']
$ ds.rename(d, {'time': 'new_time', 'temperature': 'new_temperature'})
$ ds.vars(d)
['new_temperature', 'new_time']"
	}}
	'''
	check(d, 'd', dict)
	check(mapping, 'mapping', dict, str, [str, None])
	tmp = {}
	for old in mapping.keys():
		if not require(d, 'var', old):
			continue
		var = ds.var(d, old)
		meta = ds.meta(d, old)
		tmp[old] = [var, meta]
		ds.rm(d, old)
	for old in tmp.keys():
		new = mapping[old]
		if new is None:
			continue
		var, meta = tmp[old]
		ds.var(d, new, var)
		ds.meta(d, new, meta)
	ds.rename_dim_m(d, {k: v for k, v in mapping.items() if v is not None})

def require(d, what, name, var=None, full=False):
	'''
	title: require
	caption: "Require that a variable, dimension or attribute is defined in a dataset."
	usage: "`require`(*d*, *what*, *name*, *var*=`None`, *full*=`False`)"
	desc: "If the item is not found and the mode is \\"soft\\", returns `False`. If the mode is \\"strict\\", raises `NameError`. If the mode is \\"moderate\\", produces a warning and returns `False`."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*what*: "Type of item to require. One of: \\"var\\" (variable), \\"dim\\" (dimension), \\"attr\\" (attribute) (`str`)."
		*name*: "Variable, dimension or attribute name (`str`)."
	}}
	options: {{
		*var*: "Variable name (`str`) or `None`. Applies only if *what* is \\"attr\\". If not `none`, *name* is a variable attribute name, otherwise it is a dataset attribute name."
		*full*: "Also look for items which are defined only in dataset metadata (`bool`)."
	}}
	returns: "`true` if the required item is defined in the dataset, otherwise `false` or raises an exception depending on the mode."
	examples: {{
		"Require that a variable `temperature` is defined in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.require(d, 'var', 'temperature')
True"
	}}
	'''
	check(d, 'd', dict)
	check(what, 'what', str)
	check(name, 'name', str)
	check(var, 'var', [str, None])
	if what == 'var':
		if name in ds.vars(d, full=full):
			return True
	elif what == 'dim':
		dims = ds.dims(d, var)
		if name in dims:
			return True
	elif what == 'attr':
		attrs = ds.attrs(d, var)
		if name in attrs:
			return True
	else:
		raise ValueError('invalid value of the what argument "%s"' % what)
	label = {
		'var': 'variable',
		'dim': 'dimension',
		'attr': 'attribute',
	}[what]
	err = '%s: %s not found' % (name, label)
	if ds.mode == 'strict':
		raise NameError(err)
	elif ds.mode == 'moderate':
		warn(err)
	return False

def rm(d, var):
	'''
	title: rm
	caption: "Remove a variable."
	usage: "`rm`(*d*, *var*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*var*: "Variable name (`str`)."
	}}
	returns: `None`
	examples: {{
		"Remove a variable `temperature` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.vars(d)
['temperature', 'time']
$ ds.rm(d, 'temperature')
$ ds.vars(d)
['time']"
	}}
	'''
	check(d, 'd', dict)
	check(var, 'var', str)
	var_e = ds.escape(var)
	meta = ds.meta(d)
	if var_e in d:
		del d[var_e]
	if var_e in meta:
		del meta[var_e]

def rm_attr(d, attr, var=None):
	'''
	title: rm_attr
	caption: "Remove a dataset or variable attribute."
	usage: "`rm_attr`(*d*, *attr*, *var*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*attr*: "Attribute name (`str`)."
	}}
	options: {{
		*var*: "Variable name (`str`) to remove a variable attribute or `None` to remove a dataset attribute."
	}}
	returns: `None`
	examples: {{
		"Remove an attribute `long_name` of a variable `temperature` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.attrs(d, 'temperature')
{'long_name': 'temperature', 'units': 'celsius'}
$ ds.rm_attr(d, 'long_name', var='temperature')
$ ds.attrs(d)
{'title': 'Temperature data'}"
		"Remove a dataset attribute `title` in a dataset read from `dataset.nc`.":
"$ ds.attrs(d)
{'title': 'Temperature data'}
$ ds.rm(d, 'title')
$ ds.attrs(d)
{}"
	}}
	'''
	check(d, 'd', dict)
	check(attr, 'attr', str)
	check(var, 'var', [str, None])
	if require(d, 'attr', attr, var):
		meta = ds.meta(d, '' if var is None else var)
		del meta[ds.escape(attr)]

def select(d, sel):
	'''
	title: select
	caption: "Filter dataset by a selector."
	usage: "`select`(*d*, *sel*)"
	desc: "The function subsets data of all variables in a dataset *d* by a selector *sel*. Data can be subset by a mask or a list of indexes along one or more dimensions."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*sel*: "Selector (`dict`). Selector is a dictionary where the key is a dimension name (`str`) and the value is a mask, a list of indexes (`list` or `np.array`) or an index (`int`) to subset by along the dimension."
	}}
	returns: `None`
	examples: {{
		"Subset index 0 a along dimension `time` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.var(d, 'temperature')
print(ds.var(d, 'temperature'))
$ ds.select(d, {'time': 0})
$ ds.var(d, 'temperature')
16"
		"Subset by a mask along a dimension `time` in a dataset read from `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.select(d, {'time': [False, True, True]})
$ ds.var(d, 'temperature')
[18. 21.]"
	}}
	'''
	check(d, 'd', dict)
	check(sel, 'sel', [[dict, str]])
	for var in ds.vars(d):
		select_var(d, var, sel)

def size(d, var):
	'''
	title: size
	caption: "Get variable size."
	usage: "`size`(*d*, *var*)"
	desc: "Variable size is determined based on the size of the variable data if defined, or by variable metadata attribute `.size`."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*var*: "Variable name (`str`)."
	}}
	returns: "Variable size (`list`) or `None` if not defined."
	examples: {{
		"Get the size of a variable `temperature` in `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.size(d, 'temperature')
[3]"
	}}
	'''
	check(d, 'd', dict)
	check(var, 'var', str)
	if require(d, 'var', var, full=True):
		if var in ds.vars(d):
			data = ds.var(d, var)
			return None if data is None else list(data.shape)
		else:
			meta = ds.meta(d, var)
			return list(meta.get('.size'))
	else:
		return None

def split(d, dims):
	'''
	title: split
	caption: "Split a dataset along one or more dimensions."
	usage: "`split`(*d*, *dim*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*dims*: "Dimension name (`str`) or a list of dimension names (`list` of `str`)."
	}}
	returns: "List of datasets (`list` of `dict`)."
	'''
	check(d, 'd', dict)
	check(dims, 'dims', [str, [list, str]])
	if isinstance(dims, str):
		dims = [dims]
	nn = [ds.dim(d, dim) for dim in dims]
	n = max(np.prod(nn), 1)
	dd = [{} for i in range(n)]
	for var in ds.vars(d):
		data = ds.var(d, var)
		var_meta = copy_.deepcopy(ds.meta(d, var, create=True))
		var_dims = ds.dims(d, var)
		var_size = ds.size(d, var)
		j = 0
		kk = np.ones(len(var_dims), bool)
		for dim in dims:
			try: i = var_dims.index(dim)
			except ValueError: continue
			data = np.moveaxis(data, i, j)
			j += 1
			kk[i] = False
		if j > 0:
			var_dims = (np.array(var_dims)[kk]).tolist()
			var_size = (np.array(var_size)[kk]).tolist()
			var_meta['.dims'] = var_dims
			var_meta['.size'] = var_size
			shape = data.shape
			shape = [n] + list(shape[j:])
			data = data.reshape(shape)
			aa = np.split(data, n)
			for i, a in enumerate(aa):
				ds.var(dd[i], var, a[0].copy())
				ds.meta(dd[i], var, var_meta)
		else:
			for i in range(n):
				ds.var(dd[i], var, data.copy())
				ds.meta(dd[i], var, var_meta)
	meta = copy_.deepcopy(ds.meta(d, '', create=True))
	for d1 in dd:
		ds.meta(d1, '', meta)
	return dd

def type_(d, var, *value):
	'''
	title: type
	caption: "Get or set variable type."
	usage: "`type`(*d*, *var*, \**value*)"
	desc: "Variable type is determined based on the type of the variable data if defined, or by variable metadata attribute `.type`."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*var*: "Variable name (`str`)."
		*value*: "Variable type (`str`). One of: `float32` and `float64` (32-bit and 64-bit floating-point number, resp.), `int8`, `int16`, `int32` and `int64` (8-bit, 16-bit, 32-bit and 64-bit integer, resp.), `uint8`, `uint16`, `uint32` and `uint64` (8-bit, 16-bit, 32-bit and 64-bit unsigned integer, resp.), `bool` (boolean), `str` (string) and `unicode` (Unicode)."
	}}
	returns: "Variable type (`str`) or `None` if not defined."
	examples: {{
		"Get the type of a variable `temperature` in `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.type(d, 'temperature')
'float64'"
		"Set the type of a variable `temperature` to `int64`.":
"$ ds.type(d, 'temperature', 'int64')
$ ds.type(d, 'temperature')
'int64'
$ print(ds.var(d, 'temperature'))
[16 18 21]"
	}}
	'''
	check(d, 'd', dict)
	check(var, 'var', str)
	if len(value) == 0:
		if not require(d, 'var', var, full=True):
			return None
		with ds.with_mode('soft'):
			data = ds.var(d, var)
		if data is None:
			meta = ds.meta(d, var)
			return meta.get('.type', None)
		return misc.dtype_to_type(data.dtype, data)
	elif len(value) == 1:
		check(value[0], 'value', str)
		meta = ds.meta(d, var, create=True)
		if not isinstance(value[0], str) or \
		   value[0] not in ALLOWED_TYPES:
			raise ValueError('invalid type')
		meta['.type'] = value[0]
		data = ds.var(d, var)
		if data is not None:
			dt = misc.type_to_dtype(value[0])
			data = data.astype(dt)
			if value[0] in ('str', 'unicode'):
				f = lambda x: str(x).encode('utf-8') if value[0] == 'str' \
					else str
				with np.nditer(data, op_flags=['readwrite']) as it:
				   for x in it: x[...] = f(x)
			ds.var(d, var, data)
	else:
		raise TypeError('only one value argument is expected')

def var(d, var, *value):
	'''
	title: var
	caption: "Get or set variable data."
	usage: "`var`(*d*, *var*, \**value*)"
	desc: "Variable to get or set is normalized in the following way. If the variable data are a `list` or `tuple`, they are converted to `np.ndarray`, or to `np.ma.MaskedArray` if they contain `None`, which is masked. If the variable data are `int`, `float`, `bool`, `str`, `bytes` or `np.array` with zero dimensions, they are converted to `np.generic`."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*var*: "Variable name (`str`)."
		*value*: "Variable data. If supplied, set variable data, otherwise get variable data."
	}}
	returns: "Variable data (`np.ndarray`, `np.ma.MaskedArray`, `np.generic` or `np.ma.core.MaskedConstant`) or `None` if the variable data are not defined or `value` is supplied.  Raises `ValueError` if the output dtype is not one of the types `np.float32`, `np.float64`, `np.int8`, `np.int16`, `np.int32`, `np.int64`, `np.uint8`, `np.uint16`, `np.uint32`, `np.uint64`, `np.bool`, `np.bytes<n>`, `np.str<n>`, or `np.object` for which all items are an instance of `str` or `bytes`."
	examples: {{
		"Get data of a variable `temperature` in a dataset `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ print(ds.var(d, 'temperature'))
[16. 18. 21.]"
		"Set data of a variable `temperature`.":
"$ ds.var(d, 'temperature', [17, 18, 22])
$ ds.var(d, 'temperature')
array([17, 18, 22])"
	}}
	'''
	check(d, 'd', dict)
	check(var, 'var', str)
	var_e = ds.escape(var)
	if len(value) == 0:
		if require(d, 'var', var):
			data = d[var_e]
			return normalize_var(data)
		return None
	elif len(value) == 1:
		d[var_e] = normalize_var(value[0])
	else:
		raise TypeError('only one value argument is expected')

def vars_(d, full=False):
	'''
	title: vars
	aliases: { get_vars }
	caption: "Get all variable names in a dataset."
	usage: "`get_vars`(*d*, *full*=`False`)"
	arguments: {{
		*d*: "Dataset (`dict`)."
	}}
	options: {{
		*full*: "Also return variable names which are only defined in the metadata."
	}}
	returns: "Variable names (`list` of `str`)."
	examples: {{
		"List variables in a dataset `dataset.nc`.":
"$ d = ds.read('dataset.nc')
$ ds.vars(d)
['temperature', 'time']"
		"List variables in a dataset `dataset.nc` without reading the data.":
"$ d = ds.read('dataset.nc', [], full=True)
$ ds.vars(d, full=True)
['temperature', 'time']"
	}}
	'''
	check(d, 'd', dict)
	meta = ds.meta(d)
	vars_ = list(set(meta.keys()) | set(d.keys())) if full else d.keys()
	return sorted([ds.unescape(x) for x in filter_hidden(vars_)])

vars_.aliases = ['get_vars']
get_vars = vars_
