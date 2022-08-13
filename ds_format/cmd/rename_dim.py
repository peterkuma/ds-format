from ds_format.cmd import UsageError
import ds_format as ds

def rename_dim(*args, **opts):
	'''
	title: rename_dim
	caption: "Rename a dimension."
	usage: {
		"`ds rename_dim` *old* *new* *input* *output*"
		"`ds rename_dim` { *old* *new* }... *input* *output*"
	}
	arguments: {{
		*old*: "Old dimension name."
		*new*: "New dimension name."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
		"Rename dimension `time` to `newtime` in `dataset.nc` and save the output in `output.nc`.":
"$ ds -l dataset.nc
time: 3
temperature
time
$ ds rename_dim time newtime dataset.nc output.nc
$ ds -l output.nc
newtime: 3
temperature
time"
	}}
	'''
	if len(args) < 3:
		raise UsageError('Invalid number of arguments')
	args1 = args[:-2]
	input_ = args[-2]
	output = args[-1]
	if all([type(x) is list and len(x) == 2 for x in args1]) and \
	   all([type(x[0]) is str and type(x[1]) is str for x in args1]):
		args2 = args1
	elif len(args1) == 2 and all([type(x) is str for x in args1]):
		args2 = [args1]
	else:
		raise UsageError('Invalid arguments')
	d = ds.read(input_)
	for old, new in args2:
		ds.rename_dim(d, old, new)
	ds.write(output, d)
