import json
import numpy as np
import re
import ds_format as ds

def write(*args, **opts):
	'''
	title: "write"
	caption: "Write dataset to a file."
	usage: "`ds write` *output* *var* ... *attrs*"
	arguments: {{
		*output*: "Output file."
		*var*: "Definition of a variable as `{` *name* `{` *dim* ... `}` `{` *x* ... `}` *attrs* `}`, where *name* is a variable name, *dim* is a dimension name, *x* is a value and *attrs* are variable-level attributes (key-value pairs)."
		*attrs*: "Dataset-level attributes (key-value pairs)."
	}}
	examples: {{
"Write variables time and temperature to dataset.nc.":
"ds write dataset.nc { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: \\"Temperature data\\""
	}}
	'''
	d = {'.': {}}
	output = args[0]
	variables = args[1:]
	for var in variables:
		attrs = None
		if len(var) == 3:
			name, dims, values = var
		elif len(var) == 4:
			name, dims, values, attrs = var
		else:
			raise ValueError('Invalid variable: %s' % var)
		d[name] = np.array(values)
		d['.'][name] = attrs if attrs is not None else {}
		d['.'][name]['.dims'] = dims if isinstance(dims, list) \
			else [dims]
	if len(opts.keys()) > 0:
		d['.']['.'] = opts
	ds.write(output, d)
