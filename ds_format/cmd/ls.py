import fnmatch
import numpy as np
import ds_format as ds
from ds_format import misc
import pst

def ls(*args, **opts):
	'''
	title: ls
	caption: "List variables."
	usage: {
		"`ds` [*options*] [*var*]... *input*"
		"`ds ls` [*options*] [*var*]... *input*"
	}
	arguments: {{
		*var*: "Variable name to list. glob pattern matching is performed unless `-s` is used."
		*input*: "Input file."
	}}
	options: {{
		`-s`: "Strict mode. *var* is taken as a literal string instead of a glob."
		`-l`: "Print a detailed list of variables (name and an array of dimensions), preceded with a line with dataset dimensions."
		"`a:` *attrs*": "Print variable attributes after the variable name and dimensions. *attrs* can be a string or an array."
	}}
	desc: "Lines in the output are formatted as [PST](https://github.com/peterkuma/pst). glob pattern matching follows the rules of Python [fnmatch](https://docs.python.org/3/library/fnmatch.html). Note that the pattern needs to be enclosed in quotes in order to prevent the shell from interpreting the glob."
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
	elif opts.get('s'):
		vars1 = list(set(vars_) & set(available_vars))
	else:
		vars1 = []
		for var in vars_:
			vars1 += fnmatch.filter(available_vars, var)

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
