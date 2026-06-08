import sys
import ds_format as ds
from ds_format import misc
from ds_format.misc import cmd, check, UsageError

@cmd()
def ls(*args, a=None, F=False, l=False, r={}, w={}):
	'''
	title: ls
	caption: "List variables."
	usage: "`ds` [`ls`] [*options*] [*var*]... [--] *input*"
	arguments: {{
		*var*: "Variable name to list."
		*input*: "Input file."
		*options*: "See help for ds for global options."
	}}
	options: {{
		`-l`: "Print a detailed list of variables (name, type and an array of dimensions), preceded with a line with dataset dimensions."
		"`a:` *attrs*": "Print variable attributes after the variable name and dimensions. *attrs* can be a string or an array."
	}}
	desc: "Lines in the output are formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
"Print a list of variables in `dataset.nc`.":
"$ ds ls dataset.nc
temperature
time"

"Print a detailed list of variables in `dataset.nc`.":
"$ ds ls -l dataset.nc
time: 3
temperature float64 { time }
time int64 { time }"

"Print a list of variables with an attribute `units`.":
"$ ds ls dataset.nc a: units
temperature celsius
time s"

"Print a list of variables with attributes `long_name` and `units`.":
"$ ds ls dataset.nc a: { long_name units }
temperature temperature celsius
time time s"

"Print all variables matching a glob \\"temp*\\" in `dataset.nc`.":
"$ ds ls 'temp*' dataset.nc
temperature"
	}}
	'''
	if len(args) < 1:
	    raise UsageError('invalid number of arguments')
	vars_ = args[:-1]
	input_ = args[-1]

	check(vars_, 'var', list, str, elemental=True)
	check(input_, 'input', str)
	check(a, 'a', [None, str, [list, str]])

	d = ds.read(input_, [], full=True, **r)
	available_vars = ds.vars(d, full=True)

	if len(vars_) == 0:
		vars1 = available_vars
	elif F:
		vars1 = list(set(vars_) & set(available_vars))
	else:
		vars1 = []
		for var in vars_:
			vars1 += ds.findall(d, 'var', var)

	if l:
		listed_dims = set()
		for var in vars1:
			var_dims = ds.dims(d, var)
			listed_dims |= set(var_dims)
		ds_dims = ds.dims(d, full=True, size=True)
		dims = {k: v for k, v in ds_dims.items() if k in listed_dims}
		sys.stdout.buffer.write(misc.encode(dims) + b'\n')
	for x in vars1:
		if not ds.require(d, 'var', x, full=True):
			continue
		y = [x]
		if l:
			type_ = ds.type(d, x)
			dims = ds.dims(d, x)
			y += [type_, dims]
		if a is not None:
			var_attrs = ds.attrs(d, x)
			if type(a) is list:
				y += [var_attrs.get(attr) for attr in a]
			elif type(a) is str:
				y += [var_attrs.get(a)]
		s = misc.encode(y[0] if len(y) == 1 else y)
		sys.stdout.buffer.write(s + b'\n')
