import numpy as np
import ds_format as ds
from ds_format import misc
import pst

def ls(*args, **opts):
	'''
	title: ls
	caption: "List variables."
	usage: {
		"`ds` [*var*]... *input* [*options*]"
		"`ds ls` [*var*]... *input* [*options*]"
	}
	arguments: {{
		*var*: "Variable name to list."
		*input*: "Input file."
		*options*: "See help for ds for global options."
	}}
	options: {{
		`-l`: "Print a detailed list of variables (name and an array of dimensions), preceded with a line with dataset dimensions."
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
temperature
time"

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
time: 3
temperature { time }"
	}}
	'''
	vars_ = args[:-1]
	input_ = args[-1]

	d = ds.read(input_, [], full=True)

	available_vars = ds.get_vars(d, full=True)
	if len(vars_) == 0:
		vars1 = available_vars
	elif opts.get('F'):
		vars1 = list(set(vars_) & set(available_vars))
	else:
		vars1 = []
		for var in vars_:
			vars1 += ds.findall(d, 'var', var)

	vars1 = sorted(vars1)

	if opts.get('l'):
		listed_dims = set()
		for var in vars1:
			var_dims = ds.get_dims(d, var)
			listed_dims |= set(var_dims)
		ds_dims = ds.get_dims(d, full=True)
		dims = {k: v for k, v in ds_dims.items() if k in listed_dims}
		print(pst.encode(dims).decode('utf-8'))
	for x in vars1:
		y = [x]
		if opts.get('l'):
			dims = ds.get_dims(d, x)
			y += [dims]
		if opts.get('a'):
			attrs = ds.get_attrs(d, x)
			if type(opts['a']) is list:
				y += [attrs.get(a, None) for a in opts['a']]
			elif type(opts['a']) is str:
				y += [attrs.get(opts['a'], None)]
		s = pst.encode(y, encoder=misc.encoder)
		print(s.decode('utf-8'))
