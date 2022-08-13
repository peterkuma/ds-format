import ds_format as ds
from ds_format.cmd import UsageError
from ds_format import misc
import pst

def attrs(*args, **opts):
	'''
	title: attrs
	caption: "Print attributes in a dataset."
	usage: "`ds attrs` [*var*] *input*"
	arguments: {{
		*var*: "Variable name."
		*input*: "Input file."
	}}
	desc: "The output is formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
		"Print dataset attributes in `dataset.nc`.":
"$ ds attrs dataset.nc
title: \\"Temperature data\\""
		"Print attributes of the variable `temperature` in `dataset.nc`.":
"$ ds attrs temperature dataset.nc
long_name: temperature units: celsius"
	}}
	'''
	if len(args) not in (1, 2):
		raise UsageError('Invalid number of arguments')
	var = args[0] if len(args) == 2 else None
	input_ = args[-1]
	d = ds.read(input_)
	attrs = ds.get_attrs(d, var)
	print(pst.encode(attrs, encoder=misc.encoder).decode('utf-8'))
