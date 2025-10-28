import ds_format as ds
from ds_format.misc import UsageError, check

def select(*args, **opts):
	'''
	title: select
	caption: "Select and subset variables."
	usage: "`ds select` [*var*...] [*sel*] *input* *output* [*options*]"
	desc: "select can also be used to convert between different file formats (`ds select` *input* *output*)."
	arguments: {{
		*var*: "Variable name."
		*sel*: "Selector as *dim*`:` *idx* pairs, where *dim* is a dimension name and *idx* is an index or a list of indexes as `{` *i*... `}`."
		*input*: "Input file."
		*output*: "Output file."
		*options*: "See help for ds for global options. Note that with this command *options* can only be supplied before the command name or at the end of the command line."
	}}
	options: {{
		"`at:` *value*": "At selector as *var*`:` *value* or *var*`:` `{` *value*... `}`, where *value* is the value of the variable *var* to select. The dimension indexes corresponding the variable are constrained so that a variable value closest to the value is selected."
		"`between:` *value*": "Between selector as *var*`: {` *start* *end* `}`, where *start* is the start value of the variable *var*, and *end* is the end value. The dimension indexes corresponding to the variable are constrained so that variable values in the range are selected. If the value is `none`, the range start or end is unlimited. The range start is inclusive (closed), and the end is exclusive (open)."
		"`range:` *value*": "Range selector as *dim*`: {` *start* *end* `}`, where *start* is the start index of the dimension *dim*, and *end* is the end index. If the index is `none`, the range is from the start or to the end of the dimension, respectively. Negative index values are counted from the end of the dimension. The range start is inclusive (closed), and the end is exclusive (open)."
	}}
	examples: {{
"Write data to dataset.nc.":
"$ ds set { time none time { 1 2 3 } long_name: time units: s } { temperature none time { 16. 18. 21. } long_name: temperature units: celsius } title: \\"Temperature data\\" none dataset.nc"
"List variables in dataset.nc.":
"$ ds dataset.nc
temperature
time"
"Select variable temperature from dataset.nc and write to temperature.nc.":
"$ ds select temperature dataset.nc temperature.nc"
"List variables in temperature.nc.":
"$ ds temperature.nc
temperature"
"Subset by time index 0 and write to 0.nc.":
"$ ds select time: 0 dataset.nc 0.nc"
"Print variables time and temperature in 0.nc.":
"$ ds cat time temperature 0.nc
time temperature
1 16.000000"
"Convert dataset.nc to JSON.":
"$ ds select dataset.nc dataset.json
$ cat dataset.json
{\\"time\\": [1, 2, 3], \\"temperature\\": [16.0, 18.0, 21.0], \\".\\": {\\".\\": {\\"title\\": \\"Temperature data\\"}, \\"time\\": {\\"long_name\\": \\"time\\", \\"units\\": \\"s\\", \\".dims\\": [\\"time\\"], \\".size\\": [3]}, \\"temperature\\": {\\"long_name\\": \\"temperature\\", \\"units\\": \\"celsius \\".dims\\": [\\"time\\"], \\".size\\": [3]}}}"
	}}
	'''
	if len(args) < 2:
		raise UsageError('Invalid number of arguments')
	args1 = args[:-2]
	input_ = args[-2]
	output = args[-1]

	vars_ = [x for x in args1 if type(x) is not dict]
	sel = {k: v for x in args1 if type(x) is dict for k, v in x.items()}

	check(vars_, 'var', list, str, elemental=True)
	check(input_, 'input', str)
	check(output, 'output', str)
	check(sel, 'sel', dict, str, [int, [list, int]])

	sel_opts = {
		k: opts[k][0] if type(opts[k]) is list else opts[k]
		for k in ['range', 'at', 'between']
		if k in opts
	}

	if 'range' in sel_opts:
		sel_opts['range_'] = sel_opts.pop('range')

	if not opts.get('F'):
		d = ds.read(input_, [], full=True, **sel_opts)
		vars_ = [x for var in vars_ for x in ds.findall(d, 'var', var)]
		sel = {ds.find(d, 'dim', k): v for k, v in sel.items()}
	d = ds.read(input_, vars_ if len(vars_) > 0 else None, sel, **sel_opts)
	ds.write(output, d)

select.disable_cmd_opts = True
