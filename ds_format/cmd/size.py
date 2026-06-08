import sys
from ds_format.misc import cmd, check
import ds_format as ds
from ds_format import misc

@cmd()
def size(var, input_, *, F=False, r={}, w={}):
	'''
	title: size
	caption: "Print a variable size."
	usage: "`ds size` [*options*] *var* [\\--] *input*"
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
	check(var, 'var', str)
	check(input_, 'input', str)

	d = ds.read(input_, [], full=True, **r)
	if not F:
		if var is not None:
			var = ds.find(d, 'var', var)
	size = ds.size(d, var)
	sys.stdout.buffer.write(misc.encode(size) + b'\n')
