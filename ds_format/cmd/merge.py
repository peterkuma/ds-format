import ds_format as ds

def merge(dim, *args, **opts):
	'''
	title: "merge"
	caption: "Merge datasets along a dimension dim."
	usage: "`ds merge` *dim* *input*... *output* [*options*]"
	desc: "Merge datasets along a dimension *dim*. If the dimension is not defined in the dataset, merge along a new dimension *dim*. If *new* is `none` and *dim* is not new, variables without the dimension are set with the first occurrence of the variable. If *new* is not `none` and *dim* is not new, variables without the dimension dim are merged along a new dimension *new*. If variables is not `none`, only those variables are merged along a new dimension and other variables are set to the first occurrence of the variable."
	arguments: {{
		*dim*: "Name of a dimension to merge along."
		*input*: "Input file."
		*output*: "Output file."
	}}
	options: {{
		"`new:` *value*": "Name of a new dimension."
		"`variables:` `{` *value*... `}`": "Variables to merge along a new dimension or none for all variables."
	}}
	examples: {{
"Write example data to dataset1.nc.":
"$ ds write dataset1.nc { time time { 1 2 3 } long_name: time units: s } { temperature time { 16. 18. 21. } long_name: temperature units: celsius } title: \\"Temperature data\\""

"Write example data to dataset2.nc.":
"$ ds write dataset2.nc { time time { 4 5 6 } long_name: time units: s } { temperature time { 23. 25. 28. } long_name: temperature units: celsius title: \\"Temperature data\\""

"Merge dataset1.nc and dataset2.nc and write the result to dataset.nc.":
"$ ds merge time dataset1.nc dataset2.nc dataset.nc"

"Print time and temperature variables in dataset.nc.":
"$ ds cat { time temperature } dataset.nc
1,16.0
2,18.0
3,21.0
4,23.0
5,25.0
6,28.0"
	}}
	'''
	input_ = args[:-1]
	output = args[-1]
	dd = []
	for filename in input_:
		d = ds.read(filename)
		dd.append(d)
	d = ds.op.merge(dd, dim,
		variables=opts.get('variables')
	)
	ds.write(output, d)
