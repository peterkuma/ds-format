import json
import numpy as np
import re
import ds_format as ds

def write(*args, **opts):
	d = {'.': {}}
	output = args[0]
	variables = args[1:]
	for var in variables:
		attrs = None
		if len(var) == 3:
			name, dims, values = var
		elif len(var) == 4:
			name, dims, values, attrs = var
		else:
			raise ValueError('Invalid variable: %s' % var)
		d[name] = np.array(values)
		d['.'][name] = attrs if attrs is not None else {}
		d['.'][name]['.dims'] = dims if isinstance(dims, list) \
			else [dims]
	if len(opts.keys()) > 0:	
		d['.']['.'] = opts
	ds.write(output, d)	
