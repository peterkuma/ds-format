import ds_format as ds
from ds_format.cmd import UsageError

def select(input_, output, variables=None, sel=None):
	'''
	title: "select"
	caption: "Select and subset variables."
	usage: "`ds select` *input* *output* [*variables*] [*options*]"
	desc: "select can also be used to convert between different file formats (`ds select` *input* *output*)."
	arguments: {{
		*input*: "Input file."
		*output*: "Output file."
		*variables*: "List of variables as `{` *var1* *var2* ... `}` or `none` for all. Default: `none`."
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
"$ ds write dataset.nc { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius title: \\"Temperature data\\""
"List variables in dataset.nc.":
"$ ds dataset.nc
temperature
time"
"Select variable temperature from dataset.nc and write to temperature.nc.":
"$ ds select dataset.nc temperature.nc temperature"
"List variables in temperature.nc.":
"$ ds temperature.nc
temperature"
"Subset by time index 0 and write to 0.nc.":
"$ ds select dataset.nc 0.nc sel: { time: { 0 } }"
"Print variables time and temperature in 0.nc.":
"$ ds cat { time temperature } 0.nc
1,16.0"
"Convert dataset.nc to JSON.":
"$ ds select dataset.nc dataset.json
$ cat dataset.json
{\\"time\\": [1, 2, 3], \\"temperature\\": [16.0, 18.0, 21.0], \\".\\": {\\".\\": {\\"title\\": \\"Temperature data\\"}, \\"time\\": {\\"long_name\\": \\"time\\", \\"units\\": \\"s\\", \\".dims\\": [\\"time\\"], \\".size\\": [3]}, \\"temperature\\": {\\"long_name\\": \\"temperature\\", \\"units\\": \\"celsius \\".dims\\": [\\"time\\"], \\".size\\": [3]}}}"
	}}
	'''
	sel = sel[0] if sel is not None and len(sel) > 0 else None
	d = ds.read(input_, variables, sel)
	ds.write(output, d)
