from ds_format.cmd import UsageError
import ds_format as ds

def rm(*args, **opts):
	'''
	title: rm
	caption: "Remove variables or attributes."
	usage: {
		"`ds rm` *var* *input* *output*"
		"`ds rm` *var* *attr* *input* *output*"
	}
	arguments: {{
		*var*: "Variable name, an array of variable names or `none` to remove a dataset attribute."
		*attr*: "Attribute name or an array of attribute names."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
		"Remove a variable `temperature` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm temperature dataset.nc output.nc"
		"Remove variables `time` and `temperature` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm { time temperature } dataset.nc output.nc"
		"Remove a dataset attribute `title` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm none title dataset.nc output.nc"
		"Remove an attribute `units` of a variable `temperature` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm temperature title dataset.nc output.nc"
	}}
	'''
	if len(args) not in (3, 4):
		raise UsageError('Invalid number of arguments')
	vars_ = args[0]
	attrs = args[1] if len(args) == 4 else None
	input_ = args[-2]
	output = args[-1]

	if vars_ is not None and type(vars_) is not list:
		vars_ = [vars_]
	if attrs is not None and type(attrs) is not list:
		attrs = [attrs]

	d = ds.read(input_)

	if vars_ is None:
		meta = ds.get_meta(d)
		for attr in attrs:
			if attr in meta['.']: del meta['.'][attr]
	elif attrs is None:
		for var in vars_:
			if var in d: del d[var]
	else:
		for var in vars_:
			for attr in attrs:
				meta = ds.get_meta(d, var)
				if attr in meta: del meta[attr]

	ds.write(output, d)
