from ds_format.cmd import UsageError
import ds_format as ds

def rm_attr(*args, **opts):
	'''
	title: rm_attr
	caption: "Remove an attribute in a dataset."
	usage: {
		"`ds rm_attr` [*var*] *attr* *input* *output*"
		"`ds rm_attr` [*var*] { *attr*... } *input* *output*"
	}
	arguments: {{
		*var*: "Variable name."
		*attr*: "Attribute to remove."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
		"Remove the attribute `title` from `dqtaset.nc` and save the output in `output.nc`.":
		"$ ds rm_attr title dataset.nc output.nc"
		"Remove the attribute `units` of the variable `temperature` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds rm_attr temperature title dataset.nc output.nc"
	}}
	'''
	if len(args) not in (3, 4):
		raise UsageError('Invalid number of arguments')
	var = args[0] if len(args) == 4 else None
	arg = args[-3]
	input_ = args[-2]
	output = args[-1]

	if type(arg) is list and all([type(x) is str for x in arg]):
		attrs = arg
	elif type(arg) is str:
		attrs = [arg]
	else:
		raise UsageError('Invalid arguments')

	d = ds.read(input_)
	meta = ds.get_meta(d).get('.', {}) if var is None else ds.get_meta(d, var)
	for attr in attrs:
		if attr in meta:
			del meta[attr]
	ds.write(output, d)
