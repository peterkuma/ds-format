from ds_format.cmd import UsageError
import ds_format as ds

def set_dims(*args, **opts):
	'''
	title: set_dims
	caption: "Set variable dimensions."
	usage: "`ds set_dims` *var* *dim*... *input* *output*"
	arguments: {{
		*var*: "Variable to set dimensions for."
		*dim*: "Dimension name."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
		"Set dimensions of the variable `temperature` in `dataset.nc` to (`newtime`) and save the output in `output.nc`.":
"$ ds -l dataset.nc
time: 3
temperature
time
$ ds set_dims temperature newtime dataset.nc output.nc
$ ds -l output.nc
newtime: 3
temperature
time"
	}}
	'''
	if len(args) < 3:
		raise UsageError('Invalid number of arguments')
	var = args[0]
	dims = args[1:-2]
	input_ = args[-2]
	output = args[-1]

	d = ds.read(input_)
	vars_ = ds.get_vars(d)
	if var not in vars_:
		raise ValueError('%s: variable not found' % var)
	meta = ds.get_meta(d, var)
	meta['.dims'] = dims
	ds.write(output, d)
