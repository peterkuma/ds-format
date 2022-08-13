import ds_format as ds
from ds_format.cmd import UsageError

def set_attrs(*args, **opts):
	'''
	title: set_attrs
	caption: "Set attributes in a dataset."
	usage: "`ds set_attrs` [*var*] [*attr*: *value*]... *input* *output*"
	arguments: {{
		*var*: "Variable name."
		*attr*: "Attribute to set."
		*value*: "Attribute value."
		*input*: "Input file."
		*output*: "Output file."
	}}
	examples: {{
	"Set the attribute `newtitle` to `New title` in `dataset.nc` and save the output in `output.nc`.":
	"$ ds set_attrs newtitle: \\"New title\\" dataset.nc output.nc"
	}}
	'''
	if len(args) not in (2, 3):
		raise UsageError('Invalid number of arguments')
	var = args[0] if len(args) == 3 else None
	input_ = args[-2]
	output = args[-1]
	attrs = opts
	d = ds.read(input_)
	meta = ds.get_meta(d, var)
	meta.update(attrs)
	ds.write(output, d)
