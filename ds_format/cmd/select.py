import ds_format as ds
from ds_format.cmd import UsageError

def select(*args, **opts):
	'''
	title: select
	caption: "Select and subset variables."
	usage: "`ds select` [*var*...] *input* *output* [*options*]"
	desc: "select can also be used to convert between different file formats (`ds select` *input* *output*)."
	arguments: {{
		*var*: "Variable name."
		*input*: "Input file."
		*output*: "Output file."
	}}
	options: {{
		"`sel:` `{` *dim1*: *idx1* *dim2*: *idx2* ... `}`": "Selector, where *dim* is dimension name and *idx* is a list of indexes as `{` *i1* *i2* ... `}`."
	}}
	"Supported input formats": {{
		NetCDF4: "`.nc`, `.nc4`, `.nc3`, `.netcdf`, `.hdf`, `.h5`"
		JSON: `.json`
	}}
	"Supported output formats": {{
		NetCDF4: "`.nc`, `.nc4`, `.netcdf`"
		JSON: `.json`
	}}
	examples: {{
"Write data to dataset.nc.":
"$ ds set { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: \\"Temperature data\\" none dataset.nc"
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
"$ ds select dataset.nc 0.nc sel: { time: { 0 } }"
"Print variables time and temperature in 0.nc.":
"$ ds cat time temperature 0.nc
1 16.000000"
"Convert dataset.nc to JSON.":
"$ ds select dataset.nc dataset.json
$ cat dataset.json
{\\"time\\": [1, 2, 3], \\"temperature\\": [16.0, 18.0, 21.0], \\".\\": {\\".\\": {\\"title\\": \\"Temperature data\\"}, \\"time\\": {\\"long_name\\": \\"time\\", \\"units\\": \\"s\\", \\".dims\\": [\\"time\\"], \\".size\\": [3]}, \\"temperature\\": {\\"long_name\\": \\"temperature\\", \\"units\\": \\"celsius \\".dims\\": [\\"time\\"], \\".size\\": [3]}}}"
	}}
	'''
	if len(args) < 2:
		raise UsageError('Invalid number of arguments')
	vars_ = args[:-2]
	input_ = args[-2]
	output = args[-1]
	sel = opts.get('sel')
	sel = sel[0] if sel is not None and len(sel) > 0 else None
	d = ds.read(input_, vars_ if len(vars_) > 0 else None, sel)
	ds.write(output, d)
