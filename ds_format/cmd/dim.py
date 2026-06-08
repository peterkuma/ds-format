import sys
from ds_format.misc import cmd, check
import ds_format as ds
from ds_format import misc

@cmd()
def dim(dim, input_, *, F=False, r={}, w={}):
	r'''
	title: dim
	caption: "Print dimension size."
	usage: "`ds dim` [*options*] *dim* [\\--] *input*"
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
	check(dim, 'dim', str)
	check(input_, 'input', str)
	d = ds.read(input_, [], full=True, **r)
	if F:
		dim = ds.find(d, 'dim', dim)
	dim_size = ds.dim(d, dim, full=True)
	sys.stdout.buffer.write(misc.encode(dim_size) + b'\n')
