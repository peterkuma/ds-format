from ds_format.cmd import UsageError
import ds_format as ds

def set_(*args, **opts):
	'''
	title: set
	caption: "Set or add variable data, dimensions and attributes in an existing dataset."
	usage: {
		"`ds set` *var* *dims* *data* [*attrs*]... *input* *output*"
		"`ds set` `{` *var* *dims* *data* [*attrs*]... `}`... *ds_attrs* *input* *output*"
	}
	arguments: {{
		*var*: "Variable name."
		*dims*: "Variable dimension name (if single), an array of variable dimensions (if multiple), `none` to keep original dimension or autogenerate if a new variable, or `{ }` to autogenerate new dimension names."
		*data*: "Variable data. This can be a [PST](https://github.com/peterkuma/pst)-formatted scalar or an array."
		*attrs*: "Variable attributes as *attr*: *value* pairs."
		*ds_attrs*: "Dataset attributes as *attr*: *value* pairs."
		*input*: "Input file or `none` for a new file to be created."
		*output*: "Output file."
	}}
	examples: {{
		"Set the variable `temperature` data to an array of 16.0, 18.0, 21.0.":
		"$ ds set temperature { 16. 18. 21. } dataset.nc output.nc"
		"Set the variable `temperature` dimension to "time", data to an array of 16.0, 18.0, 21.0, its attributes `long_name` to \"temperature\" and `units` to \"celsius\".":
		"$ ds set temperature time { 16. 18. 21. } long_name: temperature units: celsius"
		"Set multiple variables in a dataset and a dataset attribute.":
		"$ ds set { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: \"Temperature data\" dataset.nc output.nc"
	}}
	'''
	args1 = args[:-2]
	if all([type(x) is list and len(x) in (2, 3, 4) for x in args1]):
		ds_attrs = opts
		items = []
		for arg in args1:
			if len(arg) == 2:
				item = [arg[0], None, False, arg[1], {}]
			elif len(arg) == 3 and type(arg[2]) is dict:
				item = [arg[0], None, False, arg[1], arg[2]]
			elif len(arg) == 3:
				item = [arg[0], arg[1], True, arg[2], {}]
			else:
				item = [arg[0], arg[1], True, arg[2], arg[3]]
			items += [item]
	elif len(args1) in (2, 3):
		var = args1[0]
		dims = args1[1] if len(args1) == 3 else None
		set_dims = len(args1) == 3
		data = args1[-1]
		attrs = opts
		ds_attrs = {}
		items = [[var, dims, set_dims, data, attrs]]
	else:
		raise UsageError('Invalid arguments')
	input_ = args[-2]
	output = args[-1]

	d = ds.read(input_) if input_ is not None else {'.': {'.': {}}}
	for var, dims, set_dims, data, attrs in items:
		d[var] = data
		var_meta = ds.get_meta(d, var)
		if set_dims:
			if dims is None:
				if '.dims' in var_meta: del var_meta['.dims']
			else:
				var_meta['.dims'] = dims if type(dims) is list else [dims]
		var_meta.update(attrs)
	meta = ds.get_meta(d)
	meta['.'].update(ds_attrs)
	ds.write(output, d)
