import ds_format as ds

def merge(*args, **opts):
	if len(args) < 3:
		raise ds.cmd.UsageError('Usage: merge <dim> <input>... <output>')
	dim = args[0]
	input_ = args[1:-1]
	output = args[-1]
	dd = []
	for filename in input_:
		d = ds.read(filename)
		dd.append(d)
	d = ds.op.merge(dd, dim)
	ds.to_netcdf(output, d)
