import ds_format as ds
from ds_format.misc import check

def merge(dim, *args, **opts):
	'''
	title: merge
	caption: "Merge datasets along a dimension."
	usage: "`ds merge` *dim* *input*... *output* [*options*]"
	desc: "Merge datasets along a dimension *dim*. If the dimension is not defined in the dataset, merge along a new dimension *dim*. If *new* is `none` and *dim* is not new, variables without the dimension are set with the first occurrence of the variable. If *new* is not `none` and *dim* is not new, variables without the dimension dim are merged along a new dimension *new*. If variables is not `none`, only those variables are merged along a new dimension and other variables are set to the first occurrence of the variable."
	arguments: {{
		*dim*: "Name of a dimension to merge along."
		*input*: "Input file."
		*output*: "Output file."
		*options*: "See help for ds for global options."
	}}
	options: {{
		"`new:` *value*": "Name of a new dimension."
		"`variables:` `{` *value*... `}`": "Variables to merge along a new dimension or none for all variables."
	}}
	examples: {{
"Write example data to dataset1.nc.":
"$ ds set { time none time { 1 2 3 } long_name: time units: s } { temperature none time { 16. 18. 21. } long_name: temperature units: celsius } title: \\"Temperature data\\" none dataset1.nc"

"Write example data to dataset2.nc.":
"$ ds set { time none time { 4 5 6 } long_name: time units: s } { temperature none time { 23. 25. 28. } long_name: temperature units: celsius } title: \\"Temperature data\\" none dataset2.nc"

"Merge dataset1.nc and dataset2.nc and write the result to dataset.nc.":
"$ ds merge time dataset1.nc dataset2.nc dataset.nc"

"Print time and temperature variables in dataset.nc.":
"$ ds cat time temperature dataset.nc
time temperature
1 16.000000
2 18.000000
3 21.000000
4 23.000000
5 25.000000
6 28.000000"
	}}
	'''
	input_ = args[:-1]
	output = args[-1]

	check(dim, 'dim', str)
	check(input_, 'input', list, str)
	check(output, 'output', str)

	dd = []
	for filename in input_:
		d = ds.read(filename)
		dd.append(d)
	if not opts.get('F'):
		if len(dd) > 0:
			dim = ds.find(dd[0], 'dim', dim)
	d = ds.op.merge(dd, dim,
		variables=opts.get('variables')
	)
	ds.write(output, d)
