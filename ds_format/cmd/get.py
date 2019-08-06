import ds_format as ds
import json
from ds_format.cmd import UsageError, NumpyEncoder

def get(*args, **opts):
	if len(args) != 2:
		raise TypeError('Usage: get <path> <input>')
	path = args[0].split('/')
	input_ = args[1]

	d = ds.from_netcdf(input_, [])

	if len(path) == 2 and path[0] == '' and path[1] == '':
		j = json.dumps(d['.']['.'], sort_keys=True, indent=4, cls=NumpyEncoder)
		print(j)
	elif len(path) == 2 and path[0] == '':
		attr = path[1]
		print(d['.']['.'][attr])
	elif len(path) == 2:
		var = path[0]
		attr = path[1]
		print(d['.'][var][attr])
	elif len(path) == 1:
		var = path[0]
		j = json.dumps(d['.'][var], sort_keys=True, indent=4, cls=NumpyEncoder)
		print(j)
