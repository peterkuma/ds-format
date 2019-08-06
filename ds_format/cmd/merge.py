import ds_format as ds

def merge(dim, *args, **opts):
	input_ = args[:-1]
	output = args[-1]
	dd = []
	for filename in input_:
		d = ds.read(filename)
		dd.append(d)
	d = ds.op.merge(dd, dim)
	ds.write(output, d)
