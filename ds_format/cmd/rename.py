from ds_format.misc import cmd, UsageError, check
import ds_format as ds
from ds_format import misc

@cmd(cmd_opts=False)
def rename(*args, F=False, r={}, w={}):
	'''
	title: "rename"
	caption: "Rename variables and attributes."
	usage: {
		"`ds` [*options*] `rename` *vars* [--] *input* *output*"
		"`ds` [*options*] `rename` *var* *attrs* [--] *input* *output*"
		"`ds` [*options*] `rename` `{` *var* *attrs* `}`... [--] *input* *output*"
	}
	arguments: {{
		*var*: "Variable name, or an array of variable names whose attributes to rename, or `none` to rename dataset attributes."
		*vars*: "Pairs of old and new variable names as *oldvar*`:` *newvar*. If *newvar* is `none`, remove the variable."
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
		raise UsageError('invalid number of arguments')
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
				raise UsageError('invalid number of arguments')
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
		raise UsageError('invalid number of arguments')

	d = ds.read(input_, **r)

	for vars_, var, attrs in items:
		check(vars_, 'vars', dict, str, [str, None])
		check(var, 'var', list, [str, None], elemental=True)
		check(attrs, 'attrs', dict, str, [str, None])
		if not F:
			vars_ = {ds.find(d, 'var', k): v for k, v in vars_.items()}
			var = [x \
				for var1 in var \
				for x in (
					ds.findall(d, 'var', var1) if var1 is not None else [None]
				)]
		ds.rename_m(d, vars_)
		for var1 in var:
			if not F:
				attrs1 = {
					ds.find(d, 'attr', k, var1): v
					for var1 in var
					for k, v in attrs.items()
				}
			ds.rename_attr_m(d, attrs1, var1)
	ds.write(output, d, **w)
