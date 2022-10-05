import sys
from ds_format.misc import UsageError, check
import ds_format as ds
from ds_format import misc

def type_(*args, **opts):
	'''
	title: type
	caption: "Print a variable type."
	usage: "`ds type` *var* *input* [*options*]"
	arguments: {{
		*var*: "Variable to print the type of."
		*input*: "Input file."
		*options*: "See help for ds for global options."
	}}
	examples: {{
		"Print the type of a variable `temperature` in a dataset `dataset.nc`.":
"$ ds type temperature dataset.nc
float64"
	}}
	'''
	if len(args) != 2:
		raise UsageError('Invalid number of arguments')
	var = args[0]
	input_ = args[1]

	check(var, 'var', str)
	check(input_, 'input', str)

	d = ds.read(input_, [], full=True)
	if not opts.get('F'):
		if var is not None:
			var = ds.find(d, 'var', var)
	type_ = ds.type(d, var)
	sys.stdout.buffer.write(misc.encode(type_) + b'\n')
