import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		if isinstance(obj, np.generic):
			return np.asscalar(obj)
		return json.JSONEncoder.default(self, obj)

class UsageError(TypeError):
	pass

def check(x, name, arg, *args, elemental=False):
	def check_type(y, type_):
		return type(y) is type_ or y is None and type_ is None
	if type(x) is tuple:
		x = list(x)
	t = type(x)
	ta = type(arg)
	if ta not in (list, tuple):
		arg = [[arg] + list(args)]
	res = False
	for a in arg:
		if type(a) not in (list, tuple):
			a = [a]
		if check_type(x, a[0]):
			if a[0] in (list, tuple) and len(a) >= 2:
				res = all([check_type(y, a[1]) for y in x])
			elif a[0] is dict and len(a) >= 3:
				res = all([check_type(k, a[1]) and check_type(v, a[2]) \
					for k, v in x.items()
				])
			else:
				res = True
	if not res:
		raise ValueError('%s: invalid type' % name)
