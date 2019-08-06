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
