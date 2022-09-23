from ds_format.misc import UsageError, check
import ds_format as ds

def rename_dim(*args, **opts):
	'''
	title: rename_dim
	caption: "Rename a dimension."
	usage: {
		"`ds rename_dim` *dims* *input* *output* [*options*]"
	}
	arguments: {{
		*dims*: "Pairs of old and new dimension names as *olddim*`:` *newdim*."
		*input*: "Input file."
		*output*: "Output file."
		*options*: "See help for ds for global options. Note that with this command *options* can only be supplied before the command name or at the end of the command line."
	}}
	examples: {{
		"Rename dimension `time` to `newtime` in `dataset.nc` and save the output in `output.nc`.":
"$ ds -l dataset.nc
time: 3
temperature
time
$ ds rename_dim time: newtime dataset.nc output.nc
$ ds -l output.nc
newtime: 3
temperature
time"
	}}
	'''
	if len(args) != 3:
		raise UsageError('Invalid number of arguments')
	dims = args[0]
	input_ = args[1]
	output = args[2]

	check(dims, 'dims', dict, str, str)
	check(input_, 'input', str)
	check(output, 'output', str)

	d = ds.read(input_)
	for olddim, newdim in dims.items():
		if not opts.get('F'):
			olddim = ds.find(d, 'dim', olddim)
		ds.rename_dim(d, olddim, newdim)
	ds.write(output, d)

rename_dim.disable_cmd_opts = True
