import numpy as np
import json
import ds_format as ds
from ds_format.cmd import UsageError, NumpyEncoder

def stats(*args, **opts):
	if len(args) < 2:
		raise TypeError('Usage: stats <var> <input>...')
	var = args[0]
	input_ = args[1:]
	for filename in input_:
		d = ds.read(filename, [var])
		x = d[var].flatten()
		count = len(x)
		min_ = np.min(x)
		max_ = np.max(x)
		mean = np.mean(x)
		median = np.median(x)
		j = json.dumps({
			'count': count,
			'min': min_,
			'max': max_,
			'mean': mean,
			'median': median,
		}, cls=NumpyEncoder, sort_keys=True, indent=4)
		print(j)
