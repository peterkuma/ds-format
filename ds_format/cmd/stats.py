import numpy as np
import ds_format as ds
from ds_format import misc
from ds_format.cmd import UsageError, NumpyEncoder
import pst

def stats(*args, **opts):
	'''
	title: "stats"
	caption: "Print variable statistics."
	usage: "`ds stats` *var* *input*"
	arguments: {{
		*var*: "Variable name."
		*input*: "Input file."
	}}
	"Output description": {{
		`count`: "Number of array elements."
		`max`: "Maximum value."
		`mean`: "Sample mean."
		`median`: "Sample median."
		`min`: "Minimum value."
	}}
	desc: "The output is formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
"Print statistics of variable temperature in dataset.nc.":
"$ ds stats temperature dataset.nc
count: 3 min: 16.000000 max: 21.000000 mean: 18.333333 median: 18.000000"
	}}
	'''
	if len(args) < 2:
		raise TypeError('Usage: stats <var> <input>...')
	var = args[0]
	input_ = args[1:]
	for filename in input_:
		d = ds.read(filename, [var])
		x = d[var].flatten()
		count = len(x)
		min_ = np.min(x)
		max_ = np.max(x)
		mean = np.mean(x)
		median = np.median(x)
		print(pst.encode({
			'count': count,
			'min': min_,
			'max': max_,
			'mean': mean,
			'median': median,
		}, encoder=misc.encoder).decode('utf-8'))
