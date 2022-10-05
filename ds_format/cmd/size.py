import sys
from ds_format.misc import UsageError, check
import ds_format as ds
from ds_format import misc

def size(*args, **opts):
	'''
	title: size
	caption: "Print a variable size."
	usage: "`ds size` *var* *input* [*options*]"
	arguments: {{
		*var*: "Variable to print the size of."
		*input*: "Input file."
		*options*: "See help for ds for global options."
	}}
	examples: {{
		"Print the size of a variable `temperature` in a dataset `dataset.nc`.":
"$ ds size temperature dataset.nc
3"
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
	size = ds.size(d, var)
	sys.stdout.buffer.write(misc.encode(size) + b'\n')
