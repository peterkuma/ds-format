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

def check(x, name, arg, *args, elemental=False, fail=True):
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
		if type(x) is a[0] or x is None and a[0] is None:
			if a[0] in (list, tuple) and len(a) >= 2:
				res = all([
					check(y, name, a[1], elemental=elemental, fail=False) \
					for y in x
				])
			elif a[0] is dict and len(a) >= 3:
				res = all([
					check(k, name, a[1], elemental=elemental, fail=False) and \
					check(v, name, a[2], elemental=elemental, fail=False) \
					for k, v in x.items()
				])
			else:
				res = True
	if not res and fail:
		raise ValueError('%s: invalid type' % name)
	return res
