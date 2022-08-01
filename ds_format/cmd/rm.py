from ds_format.cmd import UsageError
import ds_format as ds

def rm(*args, **opts):
	'''
	title: "rm"
	caption: "Remove variables."
	usage: {
		"`ds rm` *var*... *input* *output*"
	}
	arguments: {{
		*var*: "Variable name."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
"Remove variable temperature from dataset.nc and save the output in output.nc.":
"$ ds rm temperature dataset.nc output.nc"

"Remove variables time and temperature from dataset.nc and save the output in output.nc.":
"$ ds rm time temperature dataset.nc output.nc"
	}}
	'''
	if len(args) < 3:
		raise ValueError('Too few arguments')
	vars_ = args[:-2]
	input_ = args[-2]
	output = args[-1]
	d = ds.read(input_)
	for var in vars_:
		if var in d:
			del d[var]
	ds.write(output, d)
