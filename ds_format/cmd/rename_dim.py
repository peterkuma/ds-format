from ds_format.cmd import UsageError
import ds_format as ds

def rename_dim(*args, **opts):
	'''
	title: rename_dim
	caption: "Rename a dimension."
	usage: {
		"`ds rename_dim` *dims* *input* *output*"
	}
	arguments: {{
		*dims*: "Pairs of old and new dimension names as *olddim*`:` *newdim*."
		*input*: "Input file."
		*output*: "Output file."
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
	if len(args) != 2:
		raise UsageError('Invalid number of arguments')
	input_ = args[0]
	output = args[1]
	dims = opts
	d = ds.read(input_)
	for olddim, newdim in opts.items():
		ds.rename_dim(d, olddim, newdim)
	ds.write(output, d)
