import json
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
		*var*: "Variable name to list."
		*input*: "Input file."
	}}
	options: {{
		`-l`: "Print a detailed list of variables (name and an array of dimensions), preceded with a line with dataset dimensions."
		"`a:` *attrs*": "Print variable attributes after the variable name and dimensions. *attrs* can be a string or an array."
	}}
	desc: "Lines in the output are formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
"Print a list of variables in dataset.nc.":
"$ ds dataset.nc
temperature
time"

"Print a detailed list of variables in dataset.nc.":
"$ ds -l dataset.nc
time: 3
temperature
time"

"Print a list of variables with an attribute `units`.":
"$ ds dataset.nc a: units
temperature celsius
time s"

"Print a list of variables with attributes `long_name` and `units`.":
"$ ds dataset.nc a: { long_name units }
temperature temperature celsius
time time s"
	}}
	'''
	vars_ = args[:-1]
	input_ = args[-1]

	d = ds.read(input_, [], full=True)
	if opts.get('l'):
		dims = ds.get_dims(d, full=True)
		all_dims = set()
		if len(vars_) > 0:
			for var in vars_:
				var_dims = ds.get_dims(d, var)
				all_dims |= set(var_dims)
			dims = {k: v for k, v in dims.items() if k in all_dims}
		print(pst.encode(dims).decode('utf-8'))
	for x in ds.get_vars(d, full=True):
		if len(vars_) > 0 and x not in vars_: continue
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
