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
		`-l`: "Print a detailed list (dimensions and long_name)."
		`-L`: "Print a more detailed list (dimensions and attributes)."
	}}
	examples: {{
"Print list variables in dataset.nc":
"$ ds dataset.nc
temperature
time"

"Print detailed list of variables in dataset.nc":
"$ ds -l dataset.nc
temperature time: 3
time time: 3"
	}}
	'''
	input_ = args
	for filename in input_:
		d = ds.read(filename, [], full=True)
		vars_ = sorted([x for x in d['.'].keys() if not x.startswith('.')])
		if opts.get('l') or opts.get('L'):
			for x in vars_:
				dims = {dim: ds.get_meta(d, x)['.size'][i]
					for i, dim in enumerate(ds.get_dims(d, x))}
				attrs = ds.get_attrs(d, x)
				y = [x]
				if opts.get('l'):
					if len(dims) > 0:
						y += [dims]
					if 'long_name' in attrs:
						y += [attrs['long_name']]
					s = pst.encode(y, encoder=misc.encoder)
				elif opts.get('L'):
					s = pst.encode([x, dims, attrs], encoder=misc.encoder)
				print(s.decode('utf-8'))
				#dims = d['.'][x]['.dims']
				#size = d['.'][x]['.size']
				#dims_s = ''
				#for i, dim in enumerate(dims):
				#	dims_s += '%s%s=%d' % (',' if i > 0 else '', dim, size[i])
				#print('%s(%s)' % (x, dims_s))
		else:
			print('\n'.join(vars_))
