from collections import Mapping, Iterable
from .op import *

def validate(d):
	if not isinstance(d, Mapping):
		raise ValueError('dataset must be a mapping')
	if '.' in d and not isinstance(d['.'], Mapping):
		raise ValueError('dataset metadata "." must be a mapping')
	if '.' in d and '.' in d['.'] and not isinstance(d['.']['.'], Mapping):
		raise ValueError('dataset attributes "./." must be a dictionary')
	dim_size = {}
	for name in get_vars(d):
		dims = get_dims(d, name)
		data = get_var(d, name)
		if len(dims) != data.ndim:
			raise ValueError('dataset variable "%s" has inconsistent number of dimensions: %d dimensions defined ("%s") but data has %d dimensions' % (name, len(dims), dims, data.ndim))
		for i, dim in enumerate(dims):
			s = data.shape[i]
			if dim in dim_size and dim_size[dim] != s:
				raise ValueError('dimension "%s" has inconsistent size between variables' % dim)
			dim_size[dim] = s
		if not isinstance(dims, Iterable):
			raise ValueError('".dims" must be iterable')
