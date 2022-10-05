import sys
from ds_format.misc import UsageError, check
import ds_format as ds
from ds_format import misc

def dims(*args, **opts):
	'''
	title: dims
	caption: "Print dimensions of a dataset or a variable."
	usage: "`ds dims` [*var*] *input* [*options*]"
	arguments: {{
		*var*: "Variable to print dimensions of."
		*input*: "Input file."
		*options*: "See help for ds for global options."
	}}
	options: {{
		"`-s`, `--size`": "If *var* is defined, print the size of dimensions as an object instead of an array of dimensions. The order is not guaranteed."
	}}
	examples: {{
		"Print dimensions of a dataset.":
"$ ds dims dataset.nc
time"
		"Print dimensions of the variable `temperature`.":
"$ ds dims temperature dataset.nc
time"

	}}
	'''
	if len(args) not in (1, 2):
		raise UsageError('Invalid number of arguments')
	var = args[0] if len(args) == 2 else None
	input_ = args[-1]
	size = opts.get('s', False) or opts.get('size', False)

	check(var, 'var', (str, None))
	check(input_, 'input', str)

	d = ds.read(input_, [], full=True)
	if not opts.get('F'):
		if var is not None:
			var = ds.find(d, 'var', var)
	dims = ds.dims(d, var, full=True, size=size)
	sys.stdout.buffer.write(misc.encode(dims) + b'\n')
