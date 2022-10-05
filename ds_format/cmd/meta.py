import sys
import json
import numpy as np
import ds_format as ds
from ds_format import misc
from ds_format.misc import UsageError, check

def meta(*args, **opts):
	'''
	title: meta
	caption: "Print dataset metadata."
	usage: "`ds meta` [*var*] *input* [*options*]"
	arguments: {{
		*input*: "Input file."
		*var*: "Variable name to print metadata for or \\".\\" to print dataset metadata. If not specified, print metadata for the whole file."
		*options*: "See help for ds for global options."
	}}
	desc: "The output is formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
"Print metadata of `dataset.nc`.":
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
	if len(args) == 1:
		var = None
		filename = args[0]
	elif len(args) == 2:
		var = args[0]
		filename = args[1]
	else:
		raise UsageError('Invalid number of arguments')

	check(var, 'var', (str, None))
	check(filename, 'input', str)

	d = ds.read(filename, [], full=True)
	if not opts.get('F'):
		if var is not None:
			var = ds.find(d, 'var', var)
	meta = ds.meta(d, var) if var != '.' else ds.meta(d, '')
	meta = {k: meta[k] for k in sorted(meta.keys())}
	sys.stdout.buffer.write(misc.encode(meta) + b'\n')
