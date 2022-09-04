from ds_format.cmd import UsageError
import ds_format as ds

def set_(*args, **opts):
	'''
	title: set
	caption: "Set variable data, dimensions and attributes in an existing or new dataset."
	usage: {
		"`ds set` *ds_attrs* *input* *output* [*options*]"
		"`ds set` *var* *dims* [*data*] [*attrs*]... *input* *output* [*options*]"
		"`ds set` `{` *var* *dims* [*data*] [*attrs*]... `}`... *ds_attrs* *input* *output* [*options*]"
	}
	arguments: {{
		*var*: "Variable name or `none` to set dataset attributes."
		*dims*: "Variable dimension name (if single), an array of variable dimensions (if multiple), `none` to keep original dimension or autogenerate if a new variable, or `{ }` to autogenerate new dimension names."
		*data*: "Variable data. This can be a [PST](https://github.com/peterkuma/pst)-formatted scalar or an array."
		*attrs*: "Variable attributes or dataset attributes if *var* is `none` as *attr*`:` *value* pairs."
		*ds_attrs*: "Dataset attributes as *attr*`:` *value* pairs."
		*input*: "Input file or `none` for a new file to be created."
		*output*: "Output file."
		*options*: "See help for ds for global options. Note that with this command *options* can only be supplied before the command name or at the end of the command line."
	}}
	examples: {{
		"Write variables `time` and `temperature` to `dataset.nc`.":
		"$ ds set { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: \\"Temperature data\\" none dataset.nc"
		"Set data of a variable `temperature` to an array of 16.0, 18.0, 21.0 in `dataset.nc` and save the output in `output.nc`.":
		"$ ds set temperature none { 16. 18. 21. } dataset.nc output.nc"
		"Set a dimension of a  variable `temperature` to "time", data to an array of 16.0, 18.0, 21.0, its attribute `long_name` to \\"temperature\\" and `units` to \\"celsius\\" in `dataset.nc` and save the output in `output.nc`.":
		"$ ds set temperature time { 16. 18. 21. } long_name: temperature units: celsius dataset.nc output.nc"
		"Set multiple variables in `dataset.nc` and save the output in `output.nc`.":
		"$ ds set { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: \\"Temperature data\\" dataset.nc output.nc"
		"Set a dataset attribute `newtitle` to `New title` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds set newtitle: \\"New title\\" dataset.nc output.nc"
		"Set an attribute `newunits` of a variable `temperature` to `K` in `dataset.nc` and save the output in `output.nc`.":
		"$ ds set temperature newunits: K dataset.nc output.nc"
	}}
	'''
	if len(args) < 2:
		raise UsageError('Invalid number of arguments')
	args1 = args[:-2]
	input_ = args[-2]
	output = args[-1]
	cmd_opts = {k: v for x in args1 if type(x) is dict \
		for k, v in x.items()}
	args1 = [x for x in args1 if type(x) is not dict]

	def process_args(args):
		if len(args) not in (2, 3, 4):
			raise UsageError('Invalid arguments')
		if type(args[-1]) is dict:
			attrs = args[-1]
			del args[-1]
		else:
			attrs = {}
		var = args[0]
		dims = args[1] if len(args) > 1 else None
		if dims is not None and type(dims) is not list:
			dims = [dims]
		data = args[2] if len(args) > 2 else None
		set_data = len(args) > 2
		return [var, dims, data, set_data, attrs]

	if len(args1) == 0:
		ds_attrs = cmd_opts
		items = []
	elif all([type(x) is list for x in args1]):
		ds_attrs = cmd_opts
		items = [process_args(arg) for arg in args1]
	else:
		ds_attrs = {}
		items = [process_args(list(args1) + [cmd_opts])]

	d = ds.read(input_) if input_ is not None else {'.': {'.': {}}}
	for var, dims, data, set_data, attrs in items:
		if not opts.get('F'):
			vars_ = ds.findall(d, 'var', var)
			if dims is not None:
				dims = [ds.find(d, 'dim', dim) for dim in dims]
		for var in vars_:
			if set_data:
				ds.var(d, var, data)
			if dims == []:
				ds.dims(d, var, None)
			elif dims is not None:
				ds.dims(d, var, dims)
			for k, v in attrs.items():
				if not opts.get('F'):
					kk = ds.findall(d, 'attr', k, var)
					for k1 in kk:
						ds.attr(d, k1, v, var=var)
				else:
					ds.attr(d, k, v, var=var)
	for k, v in ds_attrs.items():
		if not opts.get('F'):
			kk = ds.findall(d, 'attr', k)
			for k1 in kk:
				ds.attr(d, k1, v)
		else:
			ds.attr(d, k, v)
	ds.write(output, d)

set_.disable_cmd_opts = True
