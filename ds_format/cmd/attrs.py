import ds_format as ds
from ds_format.cmd import UsageError
from ds_format import misc
import pst

def attrs(*args, **opts):
	'''
	title: attrs
	caption: "Print attributes in a dataset."
	usage: "`ds attrs` [*var*] [*attr*] *input*"
	arguments: {{
		*var*: "Variable name or `none` to print a dataset attribute *attr*. If omitted, print all dataset attributes."
		*attr*: "Attribute name."
		*input*: "Input file."
	}}
	desc: "The output is formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
		"Print dataset attributes in `dataset.nc`.":
"$ ds attrs dataset.nc
title: \\"Temperature data\\""
		"Print attributes of a variable `temperature` in `dataset.nc`.":
"$ ds attrs temperature dataset.nc
long_name: temperature units: celsius"
		"Print a dataset attribute `title`.":
"$ ds attrs none title dataset.nc
\\"Temperature data\\""
		"Print an attribute units of a variable `temperature`.":
"$ ds attrs temperature units dataset.nc
celsius"
	}}
	'''
	if len(args) not in (1, 2, 3):
		raise UsageError('Invalid number of arguments')
	var = args[0] if len(args) > 1 else None
	attr = args[1] if len(args) > 2 else None
	input_ = args[-1]
	d = ds.read(input_)
	attrs = ds.get_attrs(d, var)
	if attr is not None:
		value = attrs[attr]
	else:
		value = attrs
	print(pst.encode(value, encoder=misc.encoder).decode('utf-8'))
