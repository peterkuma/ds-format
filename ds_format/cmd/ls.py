import json
import numpy as np
import ds_format as ds
from ds_format import misc
import pst

def ls(*args, **opts):
	'''
	title: "ls"
	caption: "List variables."
	usage: {
		"`ds` [*options*] *input*..."
		"`ds ls` [*options*] *input*..."
	}
	arguments: {{
		*input*: "Input file."
	}}
	options: {{
		`-l`: "Print a detailed list (name and dimensions)."
		"`-a` *attrs*": "Print given variable attributes. *attrs* can be a string or an array."
	}}
	desc: "Lines in the output are formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
"Print a list of variables in dataset.nc.":
"$ ds dataset.nc
temperature
time"

"Print a detailed list of variables in dataset.nc.":
"$ ds -l dataset.nc
temperature time: 3
time time: 3"

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
	input_ = args
	for filename in input_:
		d = ds.read(filename, [], full=True)
		vars_ = sorted([x for x in d['.'].keys() if not x.startswith('.')])
		for x in vars_:
			y = [x]
			if opts.get('l'):
				dims = {dim: ds.get_meta(d, x)['.size'][i]
					for i, dim in enumerate(ds.get_dims(d, x))}
				if len(dims) > 0:
					y += [dims]
			if opts.get('a'):
				attrs = ds.get_attrs(d, x)
				if type(opts['a']) is list:
					y += [attrs.get(a, None) for a in opts['a']]
				elif type(opts['a']) is str:
					y += [attrs.get(opts['a'], None)]
			s = pst.encode(y, encoder=misc.encoder)
			print(s.decode('utf-8'))
