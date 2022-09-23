from ds_format.misc import UsageError, check
import ds_format as ds

def rename(*args, **opts):
	'''
	title: "rename"
	caption: "Rename variables and attributes."
	usage: {
		"`ds rename` *vars* *input* *output* [*options*]"
		"`ds rename` *var* *attrs* *input* *output* [*options*]"
		"`ds rename` `{` *var* *attrs* `}`... *input* *output* [*options*]"
	}
	arguments: {{
		*var*: "Variable name, or an array of variable names whose attributes to rename, or `none` to rename dataset attributes."
		*vars*: "Pairs of old and new variable names as *oldvar*`:` *newvar*. If *newattr* is `none`, remove the attribute."
		*attrs*: "Pairs of old and new attribute names as *oldattr*`:` *newattr*. If *newattr* is `none`, remove the attribute."
		*input*: "Input file."
		*output*: "Output file."
		*options*: "See help for ds for global options. Note that with this command *options* can only be supplied before the command name or at the end of the command line."
	}}
	examples: {{
		"Rename variables `time` to `newtime` and `temperature` to `newtemperature` in `dataset.nc` and save the output in `output.nc`.":
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

	check(input_, 'input', str)
	check(output, 'output', str)

	if len(args1) == 1 and type(args1[0]) is dict:
		vars_ = args1[0]
		items = [[vars_, [], {}]]
	elif all([type(arg) is list for arg in args1]):
		items = []
		for arg in args1:
			if len(arg) != 2:
				raise UsageError('Invalid arguments')
			var = arg[0]
			if var is not None and type(var) is not list:
				var = [var]
			attrs = arg[1]
			items += [[{}, var, attrs]]
	elif len(args1) == 2:
		var = args1[0]
		if type(var) is not list: var = [var]
		attrs = args1[1]
		items = [[{}, var, attrs]]
	else:
		raise UsageError('Invalid arguments')

	d = ds.read(input_)

	for vars_, var, attrs in items:
		check(vars_, 'vars', dict, str, [str, None])
		check(var, 'var', list, [str, None], elemental=True)
		check(attrs, 'attrs', dict, str, [str, None])
		if not opts.get('F'):
			vars_ = {ds.find(d, 'var', k): v for k, v in vars_.items()}
			var = [x \
				for var1 in var \
				for x in (
					ds.findall(d, 'var', var1) if var1 is not None else [None]
				)]
		for oldvar, newvar in vars_.items():
			ds.rename(d, oldvar, newvar)
		for var1 in var:
			if not opts.get('F'):
				attrs1 = {
					ds.find(d, 'attr', k, var1): v
					for var1 in var
					for k, v in attrs.items()
				}
			for oldattr, newattr in attrs1.items():
				ds.rename_attr(d, oldattr, newattr, var=var1)
	ds.write(output, d)

rename.disable_cmd_opts = True
