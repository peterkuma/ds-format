import json
import numpy as np
import ds_format as ds

def ls(*args, **opts):
	input_ = args
	for filename in input_:
		d = ds.read(filename, [], full=True)
		vars_ = sorted([x for x in d['.'].keys() if not x.startswith('.')])
		if opts.get('l'):
			for x in vars_:
				dims = d['.'][x]['.dims']
				size = d['.'][x]['.size']
				dims_s = ','.join([
					'%s=%d' % (dim, size0)
					for dim, size0 in zip(dims, size)
				])
				print('%s(%s)' % (x, dims_s))
		else:
			print('\n'.join(vars_))
