import json
import numpy as np
import ds_format as ds
from ds_format import misc
import pst

def meta(*args, **opts):
	'''
	title: "meta"
	caption: "Print metadata."
	usage: "`ds meta` [*var*] [*input*]"
	arguments: {{
		*input*: "Input file."
		*var*: "Variable name to print metadata for. If not specified, print metadata for the whole file."
	}}
	desc: "The output is formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
"Print metadata of dataset.nc.":
"$ ds meta dataset.nc
.: {{
	title: \\"Temperature data\\"
}}
time: {{
	long_name: time
	units: s
	.dims: { time }
	.size: { 3 }
}}
temperature: {{
	long_name: temperature
	units: celsius
	.dims: { time }
	.size: { 3 }
}}"
	}}
	'''
	if len(args) == 0:
		return
	elif len(args) == 1:
		var = None
		filename = args[0]
	elif len(args) == 2:
		var = args[0]
		filename = args[1]
	else:
		raise ValueError('Too many arguments')
	d = ds.read(filename, [], full=True)
	info = ds.get_meta(d, var)
	s = pst.encode(info, encoder=misc.encoder, indent=True)
	print(s.decode('utf-8'))
