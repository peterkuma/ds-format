import json
import numpy as np
import ds_format as ds

def meta(*args, **opts):
	input_ = args
	for filename in input_:
		d = ds.read(filename, [], full=True)
		info = d['.']
		j = json.dumps(info, sort_keys=True, indent=4, cls=ds.cmd.NumpyEncoder)
		print(j)
