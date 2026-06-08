from ds_format.misc import cmd, check
import ds_format as ds
from ds_format import misc

@cmd(cmd_opts=False)
def rename_dim(dims, input_, output, *, F=False, r={}, w={}):
	'''
	title: rename_dim
	caption: "Rename a dimension."
	usage: {
		"`ds` [*options*] `rename_dim` *dims* [--] *input* *output*"
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
	check(dims, 'dims', dict, str, str)
	check(input_, 'input', str)
	check(output, 'output', str)

	d = ds.read(input_, **r)
	mapping = {}
	for olddim, newdim in dims.items():
		if not F:
			olddim = ds.find(d, 'dim', olddim)
		mapping[olddim] = newdim
	ds.rename_dim_m(d, mapping)
	ds.write(output, d, **w)
