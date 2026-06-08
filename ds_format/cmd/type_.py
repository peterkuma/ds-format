import sys
from ds_format.misc import cmd, check
import ds_format as ds
from ds_format import misc

@cmd()
def type_(var, input_, *, F=False, r={}, w={}):
	r'''
	title: type
	caption: "Print a variable type."
	usage: "`ds type` [*options*] *var* [\\--] *input*"
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
	check(var, 'var', str)
	check(input_, 'input', str)

	d = ds.read(input_, [], full=True, **r)
	if not F:
		if var is not None:
			var = ds.find(d, 'var', var)
	type_ = ds.type(d, var)
	sys.stdout.buffer.write(misc.encode(type_) + b'\n')
