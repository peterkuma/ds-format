from ds_format.misc import UsageError, check
import ds_format as ds

def rm(*args, **opts):
	'''
	title: rm
	caption: "Remove variables or attributes."
	usage: {
		"`ds rm` *var* *input* *output* [*options*]"
		"`ds rm` *var* *attr* *input* *output* [*options*]"
	}
	arguments: {{
		*var*: "Variable name, an array of variable names or `none` to remove a dataset attribute."
		*attr*: "Attribute name or an array of attribute names."
		*input*: "Input file."
		*output*: "Output file."
		*options*: "See help for ds for global options."
	}}
	examples: {{
		"Remove a variable `temperature` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm temperature dataset.nc output.nc"
		"Remove variables `time` and `temperature` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm { time temperature } dataset.nc output.nc"
		"Remove a dataset attribute `title` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm none title dataset.nc output.nc"
		"Remove an attribute `units` of a variable `temperature` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm temperature units dataset.nc output.nc"
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

	check(vars_, 'var', [None, [list, str]], elemental=True)
	check(attrs, 'attr', [None, [list, str]])
	check(input_, 'input', str)
	check(output, 'output', str)

	d = ds.read(input_)

	if not opts.get('F'):
		if vars_ is not None:
			vars_ = [x for var in vars_ for x in ds.findall(d, 'var', var)]
		if attrs is not None:
			if vars_ is None:
				attrs = [x for attr in attrs \
					for x in ds.findall(d, 'attr', attr)]
			else:
				attrs = [
					x
					for attr in attrs
					for var in vars_
					for x in ds.findall(d, 'attr', attr, var)
				]

	if vars_ is None:
		for attr in attrs:
			ds.rm_attr(d, attr)
	elif attrs is None:
		for var in vars_:
			ds.rm(d, var)
	else:
		for var in vars_:
			for attr in attrs:
				ds.rm_attr(d, attr, var=var)

	ds.write(output, d)
