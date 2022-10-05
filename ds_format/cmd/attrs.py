import sys
import ds_format as ds
from ds_format.misc import UsageError, check
from ds_format import misc

def attrs(*args, **opts):
	'''
	title: attrs
	caption: "Print attributes in a dataset."
	usage: "`ds attrs` [*var*] [*attr*] *input* [*options*]"
	arguments: {{
		*var*: "Variable name or `none` to print a dataset attribute *attr*. If omitted, print all dataset attributes."
		*attr*: "Attribute name."
		*input*: "Input file."
		*options*: "See help for ds for global options."
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

	check(var, 'var', (str, None))
	check(attr, 'attr', (str, None))
	check(input_, 'input', str)

	d = ds.read(input_, [], full=True)

	if not opts.get('F'):
		if var is not None:
			var = ds.find(d, 'var', var)
		if attr is not None:
			attr = ds.find(d, 'attr', attr, var)

	if attr is not None:
		value = ds.attr(d, attr, var=var)
	else:
		value = ds.attrs(d, var)
	sys.stdout.buffer.write(misc.encode(value) + b'\n')
