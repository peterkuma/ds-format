from collections import Mapping, Iterable
import ds_format as ds
from .op import gen_dims

def validate(d):
	if not isinstance(d, dict):
		raise ValueError('dataset must be an instance of dict')
	if '.' in d and not isinstance(d['.'], dict):
		raise ValueError('dataset metadata "." must be an instance of dict')
	if '.' in d and '.' in d['.'] and not isinstance(d['.']['.'], dict):
		raise ValueError('dataset attributes "./." must be an instance of dict')
	dim_size = {}
	for name in ds.vars(d):
		dims = ds.dims(d, name)
		data = ds.var(d, name)
		if data is not None and len(dims) != data.ndim:
			raise ValueError('dataset variable "%s" has inconsistent number of dimensions: %d dimensions defined ("%s") but data has %d dimensions' % (name, len(dims), dims, data.ndim))
		for i, dim in enumerate(dims):
			s = data.shape[i]
			if dim in dim_size and dim_size[dim] != s:
				raise ValueError('dimension "%s" has inconsistent size between variables' % dim)
			dim_size[dim] = s
		if not (dims is None or isinstance(dims, (list, tuple))):
			raise ValueError('".dims" must be an instance of list or tuple or None')
