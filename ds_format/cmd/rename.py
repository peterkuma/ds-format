from ds_format.cmd import UsageError
import ds_format as ds

def rename(*args, **opts):
	'''
	title: "rename"
	caption: "Rename variables."
	usage: {
		"`ds rename` *old* *new* *input* *output*"
		"`ds rename` { *old* *new* }... *input* *output*"
	}
	arguments: {{
		*old*: "Old variable name."
		*new*: "New variable name."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
"Rename variable time to a in dataset.nc and save the output in output.nc.":
"$ ds rename time a dataset.nc output.nc"

"Rename variable `time` to `a and `temperature` to `b` in dataset.nc and save the output in output.nc.":
"$ ds rename { time a } { temperature b } dataset.nc output.nc"
	}}
	'''
	if len(args) < 3:
		raise ValueError('too few arguments')
	args1 = args[:-2]
	input_ = args[-2]
	output = args[-1]
	d = ds.read(input_)

	def rename1(old, new):
		if not type(old) is str and type(new) is str:
			raise TypeError('invalid type of arguments')
		if old in d:
			d[new] = d[old]
		else:
			raise ValueError('variable "%s" not found' % old)
		del d[old]

	if all(type(arg) is list for arg in args1):
		for vars_ in args1:
			if len(vars_) != 2:
				raise TypeError('invalid type of arguments')
			rename1(vars_[0], vars_[1])
	else:
		rename1(args1[0], args1[1])
	ds.write(output, d)
