import sys
import numpy as np
import ds_format as ds
from ds_format import misc
from ds_format.misc import UsageError, check

def stats(*args, **opts):
	'''
	title: stats
	caption: "Print variable statistics."
	usage: "`ds stats` *var* *input* [*options*]"
	arguments: {{
		*var*: "Variable name."
		*input*: "Input file."
		*options*: "See help for ds for global options."
	}}
	"Output description": {{
		`count`: "Number of array elements."
		`max`: "Maximum value."
		`mean`: "Sample mean."
		`median`: "Sample median."
		`min`: "Minimum value."
		`std`: "Standard deviation."
		`p68`: "68% confidence interval calculated using percentiles."
		`p95`: "95% confidence interval calculated using percentiles."
		`p99`: "99% confidence interval calculated using percentiles."
	}}
	desc: "NaNs are ignored in all statistics except for `count`. The output is formatted as [PST](https://github.com/peterkuma/pst)."
	examples: {{
"Print statistics of variable temperature in dataset.nc.":
"$ ds stats temperature dataset.nc
count: 3 min: 16.000000 max: 21.000000 mean: 18.333333 median: 18.000000 std: 2.054805 p68: { 16.640000 20.040000 } p95: { 16.100000 20.850000 } p99: { 16.020000 20.970000 }"
	}}
	'''
	if len(args) != 2:
		raise UsageError('Invalid number of arguments')
	var = args[0]
	input_ = args[1]

	check(var, 'var', str)
	check(input_, 'input', str)

	if not opts.get('F'):
		d = ds.read(input_, [], full=True)
		var = ds.find(d, 'var', var)
	d = ds.read(input_, [var])
	x = ds.var(d, var)
	if x is None:
		return
	x = x.flatten()
	count = len(x)
	min_ = np.nanmin(x)
	max_ = np.nanmax(x)
	mean = np.nanmean(x)
	median = np.nanmedian(x)
	std = np.nanstd(x)
	percentile = [[0.5*(100 - p), 100 - 0.5*(100 - p)] for p in [68, 95, 99]]
	p68, p95, p99 = np.nanpercentile(x, percentile)

	sys.stdout.buffer.write(misc.encode({
		'count': count,
		'min': min_,
		'max': max_,
		'mean': mean,
		'median': median,
		'std': std,
		'p68': p68,
		'p95': p95,
		'p99': p99,
	}) + b'\n')
