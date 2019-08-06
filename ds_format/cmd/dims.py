import ds_format as ds

def dims(*args, **opts):
	if len(args) == 0:
		raise TypeError('Usage: dims <input>...')
	input_ = args
	for filename in input_:
		d = ds.read(filename, [])
		dims = ds.get_dims(d)
		for dim in dims:
			print(dim)
		out = {x: for x in dims}
		j = json.dumps(out, indent=4)
		print(j)
