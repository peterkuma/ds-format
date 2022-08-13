from ds_format.cmd import UsageError
import ds_format as ds

def rename_attr(*args, **opts):
	'''
	title: rename_attr
	caption: "Rename an attribute in a dataset."
	usage: {
		"`ds rename_attr` [*var*] *old* *new* *input* *output*"
		"`ds rename_attr` [*var*] { *old* *new* }... *input* *output*"
	}
	arguments: {{
		*var*: "Variable name."
		*old*: "Old attribute name."
		*new*: "New attribute name."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
		"Rename the attribute `title` in `dataset.nc` to `newtitle` and save the output in `output.nc`.":
		"$ ds rename_attr title newtitle dataset.nc output.nc"
		"Rename the attribute `units` of the variable `temperature` in `dataset.nc` to `newunits` and save the output in `output.nc`.":
		"$ ds rename_attr temperature units newunits dataset.nc output.nc"
	}}
	'''
	if len(args) < 3:
		raise UsageError('Invalid number of arguments')
	args1 = args[:-2]
	input_ = args[-2]
	output = args[-1]

	if len(args1) in (2, 3) and all([type(x) is str for x in args1]):
		var = args1[0] if len(args1) == 3 else None
		attrs = [[args1[-2], args1[-1]]]
	elif len(args1) > 1 and \
	   type(args1[0]) is str and \
	   all([type(x) is list for x in args1[1:]]) and \
	   all([type(x[0]) is str and type(x[1]) is str for x in args1[1:]]):
		var = args1[0]
		attrs = args1[1:]
	elif all([type(x) is list for x in args1]) and \
	     all([type(x[0]) is str and type(x[1]) is str for x in args1]):
		var = None
		attrs = args1
	else:
		raise UsageError('Invalid arguments')

	d = ds.read(input_)
	meta = ds.get_meta(d)['.'] if var is None else ds.get_meta(d, var)
	for old, new in attrs:
		if old in meta:
			meta[new] = meta[old]
			del meta[old]
	ds.write(output, d)
