import sys
from ds_format.misc import UsageError, check
import ds_format as ds
from ds_format import misc

def dim(*args, **opts):
	'''
	title: dim
	caption: "Print dimension size."
	usage: "`ds dim` *dim* *input* [*options*]"
	arguments: {{
		*dim*: "Dimension name."
		*input*: "Input file."
		*options*: "See help for ds for global options."
	}}
	examples: {{
		"Print size of the dimension `time` in dataset `dataset.nc`.":
"$ ds dim time dataset.nc
3"
	}}
	'''
	if len(args) != 2:
		raise UsageError('Invalid number of arguments')
	dim = args[0]
	input_ = args[1]
	check(dim, 'dim', str)
	check(input_, 'input', str)
	d = ds.read(input_, [], full=True)
	if opts.get('F'):
		dim = ds.find(d, 'dim', dim)
	dim_size = ds.dim(d, dim, full=True)
	sys.stdout.buffer.write(misc.encode(dim_size) + b'\n')
