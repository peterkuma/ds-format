from ds_format.cmd import UsageError
import ds_format as ds

def rename(*args, **opts):
	'''
	title: "rename"
	caption: "Rename variables and attributes."
	usage: {
		"`ds rename` *vars* *input* *output*"
		"`ds rename` *var* *attrs* *input* *output*"
		"`ds rename` `{` *var* *attrs* `}`... *input* *output*"
	}
	arguments: {{
		*var*: "Variable name or an array of variable names whose attributes to rename or `none` to change dataset attributes."
		*vars*: "Pairs of old and new variable names as *var*`:` *newvar*. If *newattr* is `none`, remove the attribute."
		*attrs*: "Pairs of old and new attribute names as *attr*`:` *newattr*. If *newattr* is `none`, remove the attribute."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
		"Rename variable `time` to `newtime` and `temperature` to `newtemperature` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rename time: newtime temperature: newtemperature dataset.nc output.nc"
		"Rename a dataset attribute `title` to `newtitle` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rename none title: newtitle dataset.nc output.nc"
		"Rename an attribute `units` of a variable `temperature` to `newunits` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rename temperature units: newunits dataset.nc output.nc"
	}}
	'''
	if len(args) < 2:
		raise UsageError('Invalid number of arguments')
	args1 = list(args[:-2])
	input_ = args[-2]
	output = args[-1]

	if all([type(arg) is list for arg in args1]):
		items = []
		for arg in args1:
			if len(arg) != 2:
				raise UsageError('Invalid arguments')
			var = arg[0]
			if type(var) is not list: var = [var]
			attrs = arg[1]
			items += [[{}, var, attrs]]
	elif len(args1) == 0:
		vars_ = opts
		items = [[vars_, None, {}]]
	elif len(args1) == 1:
		var = args1[0]
		if type(var) is not list: var = [var]
		attrs = opts
		items = [[{}, var, attrs]]
	else:
		raise UsageError('Invalid arguments')

	d = ds.read(input_)

	for vars_, var, attrs in items:
		for oldvar, newvar in vars_.items():
			if newvar is not None:
				if oldvar in d:
					ds.rename(d, oldvar, newvar)
			else:
				del d[oldvar]
		for var1 in var:
			meta = ds.get_meta(d)['.'] if var1 is None \
				else ds.get_meta(d, var1)
			for oldattr, newattr in attrs.items():
				if oldattr in meta:
					if newattr is not None:
						meta[newattr] = meta[oldattr]
					del meta[oldattr]
		ds.write(output, d)
