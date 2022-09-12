import ds_format as ds
from collections import Mapping, Iterable
import copy as copy_
import numpy as np
import datetime as dt
import fnmatch
from . import misc
from warnings import warn

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
			idxs = np.array(idxs) if type(idxs) in (list, tuple) else idxs
			if isinstance(idxs, np.ndarray) and idxs.dtype == np.bool:
				idxs = np.nonzero(idxs)[0]
			if dim in var_dims:
				i = var_dims.index(dim)
				data = ds.var(d, var)
				ds.var(d, var, np.take(data, idxs, axis=i))
				if not isinstance(idxs, np.ndarray):
					var_dims.remove(dim)

def filter_hidden(x):
	if isinstance(x, Mapping):
		return {k: v for k, v in x.items() if not k.startswith('.')}
	if isinstance(x, Iterable):
		return [k for k in x if not k.startswith('.')]
	return x

def gen_dims(d, var):
	data = ds.var(d, var)
	var_meta = ds.meta(d, var)
	if data is not None:
		ndim = data.ndim
	elif '.size' in var_meta:
		ndim = len(var_meta['.size'])
	else:
		ndim = 0
	return [var + ('_%d' % i) for i in range(1, ndim + 1)]

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

def merge_var(dd, var, dim):
	if len(dd) == 0:
		return None, None
	x0 = ds.var(dd[0], var)
	var_meta0 = ds.meta(dd[0], var)
	dims0 = ds.dims(dd[0], var)
	var_meta = copy_.deepcopy(var_meta0)
	if dim in dims0:
		i = dims0.index(dim)
		x = np.concatenate(
			[ds.var(d, var) for d in dd if ds.dims(d, var) == dims0],
			axis=i
		)
	else:
		var_meta['.dims'] = [dim] + dims0
		x = np.stack([ds.var(d, var) for d in dd if ds.dims(d, var) == dims0])
	return x, var_meta

def copy(d):
	d2 = {}
	for var in ds.vars(d):
		data = ds.var(d, var)
		ds.var(d2, var, data)
	meta = ds.meta(d)
	ds.meta(d2, None, copy_.deepcopy(meta))
	return d2

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
	'''
	if len(value) > 1:
		raise TypeError('only one value argument is expected')
	if len(value) == 0:
		if require(d, 'attr', attr, var):
			attrs = ds.attrs(d, var)
			return attrs[attr]
	else:
		meta = ds.meta(d, '' if var is None else var, create=True)
		meta[ds.escape(attr)] = value[0]

def attrs(d, var=None, *value):
	'''
	title: attrs
	caption: "Get variable or dataset attributes."
	usage: "`attrs`(*d*, *var*=`None`, \**value*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*value*: "Attributes to set (`dict`). If supplied, set attributes to *value*, otherwise get attributes."
	}}
	options: {{
		*var*: "Variable name (`str`) or `None` to get dataset attributes."
	}}
	returns: "Attributes (`dict`)."
	'''
	if len(value) == 0:
		meta = ds.meta(d, '' if var is None else var)
		return {ds.unescape(k): v for k, v in filter_hidden(meta).items()}
	elif len(value) == 1:
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
	'''
	if require(d, 'dim', dim):
		return dims(d, full=full, size=True)[dim]
	return 0

def dims(d, var=None, *value, full=False, size=False):
	'''
	title: dims
	aliases: { get_dims }
	usage: "`dims`(*d*, *var*=`None`, \**value*, *full*=`False`, *size*=`False`)"
	caption: "Get dataset or variable dimensions or set variable dimensions."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*value*: "A list of dimensions (`list` of `str`) or `None`. If supplied, set variable dimensions, otherwise get dataset or variable dimensions. If `None`, remove variable dimensions (will be set to autogenerated names on write)."
	}}
	options: {{
		*var*: "Variable name (`str`) or `None` to get dataset dimensions."
		*full*: "Get variable dimensions even if the variable is only defined in the matadata (`bool`)."
		*size*: "Return a dictionary containing dimension sizes."
	}}
	returns: "Dimension names (`list` of `str`) or a dictionary of dimension sizes (`dict`)."
	'''
	if len(value) > 1:
		raise TypeError('only one value argument is expected')
	if len(value) == 0:
		dims = {}
		if var is None:
			for name in ds.vars(d, full):
				var_dims = ds.dims(d, name, size=True)
				for k, v in var_dims.items():
					dims[k] = dims.get(k) if v is None else v
		else:
			meta = ds.meta(d, var)
			if not size:
				dims = meta.get('.dims', gen_dims(d, var))
				if type(dims) is list:
					return dims
				elif type(dims) is tuple:
					return list(dims)
				else:
					return [dims]
			data = ds.var(d, var)
			var_size = meta.get('.size')
			var_dims = meta.get('.dims', gen_dims(d, var))
			for i, dim in enumerate(var_dims):
				if data is not None:
					dims[dim] = data.shape[i]
				elif var_size is not None:
					dims[dim] = var_size[i]
				else:
					dims[dim] = None
		return dims
	else:
		meta = ds.meta(d, var, create=True)
		if value[0] is None:
			if '.dims' in meta:
				del meta['.dims']
		else:
			meta['.dims'] = value[0]

get_dims = dims
dims.aliases = ['get_dims']

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
	'''
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
	'''
	if what == 'var':
		names = ds.vars(d, full=True)
	elif what == 'attr':
		names = ds.attrs(d, var)
	elif what == 'dim':
		names = list(ds.dims(d, var, full=True).keys())
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
	'''
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

def merge(dd, dim, new=None, variables=None):
	'''
	title: merge
	caption: "Merge datasets along a dimension."
	usage: "`merge`(*dd*, *dim*, *new*=`None`, *variables*=`None`)"
	desc: "Merge datasets along a dimension *dim*. If the dimension is not defined in the dataset, merge along a new dimension *dim*. If *new* is None and *dim* is not new, variables without the dimension are set with the first occurrence of the variable. If *new* is not None and *dim* is not new, variables without the dimension *dim* are merged along a new dimension *new*. If *variables* is not None, only those variables are merged along a new dimension and other variables are set to the first occurrence of the variable."
	arguments: {{
		*dd*: "Datasets (`list`)."
		*dim*: "Name of a dimension to merge along (`str`)."
	}}
	options: {{
		*new*: "Name of a new dimension (`str`) or `None`."
		*variables*: "Variables to merge along a new dimension (`list`) or `None` for all variables."
	}}
	returns: "A dataset (`dict`)."
	'''
	dx = {'.': {'.': {}}}
	vars_ = list(set([x for d in dd for x in ds.vars(d)]))
	dims = [k for d in dd for k in ds.dims(d)]
	is_new = dim not in dims
	for var in vars_:
		var_dims = ds.dims(dd[0], var)
		if is_new and (variables is None or var in variables) or \
		   dim in var_dims:
			x, meta = merge_var(dd, var, dim)
		elif new is not None and (variables is None or var in variables):
			x, meta = merge_var(dd, var, new)
		else:
			x, meta = ds.var(dd[0], var), ds.meta(dd[0], var)
		ds.var(dx, var, x)
		ds.meta(dx, var, meta)
	for d in dd:
		if '.' in d['.']:
			dx['.']['.'].update(d['.']['.'])
	return dx

def meta(d, var=None, meta=None, create=False):
	'''
	title: meta
	aliases: { get_meta }
	caption: "Get or set dataset or variable metadata."
	usage: "`meta`(*d*, *var*=`None`, *meta*=`None`, *create*=`False`)"
	arguments: {{
		*d*: "Dataset (`dict`)."
	}}
	options: {{
		*var*: "Variable name (`str`), or `None` to get dataset metadata, or an empty string to get dataset attributes."
		*meta*: "Metadata to set (`dict`) or `None` to get metadata."
		*create*: "Create (modifyable/bound) metadata dictionary in the dataset if not defined (`bool`). If `False`, the returned dictionary is an empty unbound dictionary if not present in the dataset."
	}}
	returns: "Metadata (`dict`)."
	'''
	var_e = ds.escape(var)

	if meta is not None:
		if var is None:
			d['.'] = meta
		else:
			ds_meta = ds.meta(d, create=True)
			ds_meta[var_e] = meta
		return meta

	if var is None:
		if '.' in d:
			return d['.']
		if create:
			d['.'] = {}
			return d['.']
		return {}

	if var == '':
		meta = ds.meta(d, create=create)
		if '.' in meta:
			return meta['.']
		if create:
			meta['.'] = {}
			return meta['.']
		return {}

	meta = ds.meta(d, create=create)
	if var_e in meta:
		return meta[var_e]
	if create:
		meta[var_e] = {}
		return meta[var_e]
	require(d, 'var', var, full=True)
	return {}

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
	'''
	new_e = ds.escape(new)
	old_e = ds.escape(old)
	if require(d, 'var', old):
		if old == new:
			return
		if new is not None:
			d[new_e] = d[old_e]
			d['.'][new_e] = d['.'][old_e]
		del d[old_e]
		del d['.'][old_e]
		if new is not None:
			rename_dim(d, old, new)

def rename_attr(d, old, new, var=None):
	'''
	title: rename_attr
	caption: "Rename a dataset or variable attribute."
	arguments: {{
		*d*: "Dataset (`dict`)."
		*old*: "Old attribute name (`str`)."
		*new*: "New attribute name (`str`)."
	}}
	options: {{
		*var*: "Variable name (`str`) to rename a variable attribute or `None` to rename a dataset attribute."
	}}
	returns: `None`
	'''
	old_e = ds.escape(old)
	new_e = ds.escape(new)
	if require(d, 'attr', old, var):
		meta = ds.meta(d, '' if var is None else var)
		if new is not None:
			meta[new_e] = meta[old_e]
		del meta[old_e]

def rename_dim(d, old, new):
	'''
	title: rename
	caption: "Rename a dimension."
	usage: "`rename_dim`(*d*, *old*, *new*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*old*: "Old dimension name (`str`)."
		*new*: "New dimension name (`str`)."
	}}
	returns: `None`
	'''
	if old == new:
		return
	for var in ds.vars(d, full=True):
		dims = ds.dims(d, var)
		dirty = False
		for i, dim in enumerate(dims):
			if dim == old:
				dims[i] = new
				dirty = True
		if dirty:
			ds.dims(d, var, dims)

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
	'''
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
	'''
	if require(d, 'var', var):
		del d[ds.escape(var)]

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
	'''
	if require(d, 'attr', attr, var):
		meta = ds.meta(d, '' if var is None else var)
		del meta[ds.encode(attr)]

def select(d, sel):
	'''
	title: select
	caption: "Filter dataset by a selector."
	usage: "`select`(*d*, *sel*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*sel*: "Selector (`dict`). Selector is a dictionary where each key is a dimension name and value is a mask to apply along the dimension or a list of indexes."
	}}
	returns: `None`
	'''
	for var in ds.vars(d):
		select_var(d, var, sel)

def var(d, var, *value):
	'''
	title: var
	caption: "Get or set variable data."
	usage: "`var`(*d*, *var*, \**value*)"
	arguments: {{
		*d*: "Dataset (`dict`)."
		*var*: "Variable name (`str`)."
		*value*: "Variable data. If supplied, set variable data, otherwise get variable data."
	}}
	returns: "Variable data as a numpy array (`np.ndarray`) or `None` if the variable data are not defined or `value` is supplied."
	'''
	var_e = ds.escape(var)
	if len(value) > 1:
		raise TypeError('only one value argument is expected')
	if len(value) == 0:
		if require(d, 'var', var):
			data = d[var_e]
			if isinstance(data, np.ndarray):
				return data
			else:
				data = np.array(data)
				mask = data == None
				if np.any(mask):
					data[mask] = 0
					dtype = np.array(data.flatten().tolist()).dtype
					data = np.ma.array(data, dtype, mask=mask)
				return data
		return None
	else:
		d[var_e] = value[0]

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
	'''
	meta = ds.meta(d)
	vars_ = list(set(meta.keys()) | set(d.keys())) if full else d.keys()
	return [ds.unescape(x) for x in filter_hidden(vars_)]

vars_.aliases = ['get_vars']
get_vars = vars_
