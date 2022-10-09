import sys
import numpy as np
from ds_format.misc import UsageError, check
import ds_format as ds
from ds_format import misc
import aquarius_time as aq

def cat(*args, **opts):
	'''
	title: cat
	caption: "Print variable data."
	usage: {
		"`ds cat` *var* *input* [*options*]"
		"`ds cat` *var*... *input* [*options*]"
	}
	arguments: {{
		*var*: "Variable name."
		*input*: "Input file."
		*options*: "See help for ds for global options."
	}}
	options: {{
		`-h`: "Print human-readable values (time as ISO 8601)."
		`--jd`: "Convert time variables to Julian date (see [Aquarius Time](https://github.com/peterkuma/aquarius-time))."
	}}
	desc: "Data are printed by the first index, one item per line, formatted as [PST](https://github.com/peterkuma/pst)-formatted. If multiple variables are selected, items at a given index from all variables are printed on the same line as an array. The first line is a header containing a list of variables. Missing values are printed as empty rows (if printing one single dimensional variable) or as `none`."
	examples: {{
"Print temperature values in dataset.nc.":
"$ ds cat temperature dataset.nc
temperature
16.000000
18.000000
21.000000"

"Print time and temperature values in dataset.nc.":
"$ ds cat time temperature dataset.nc
time temperature
1 16.000000
2 18.000000
3 21.000000"
	}}
	'''
	if len(args) < 1:
		raise UsageError('Invalid number of arguments')
	vars_ = args[:-1]
	input_ = args[-1]

	check(vars_, 'var', list, str, elemental=True)
	check(input_, 'input', str)

	if not opts.get('F'):
		d = ds.read(input_, [], full=True)
		vars_ = [x for var in vars_ for x in ds.findall(d, 'var', var)]

	d = ds.read(input_, vars_,
		full=False,
		jd=(opts.get('jd') or opts.get('h')),
	)
	if len(vars_) == 0:
		return
	dims = [ds.dims(d, var) for var in vars_]
	if not all([dim == dims[0] for dim in dims]):
		raise ValueError('incompatible dimensions')

	vars1 = vars_[0] if len(vars_) == 1 else vars_
	sys.stdout.buffer.write(misc.encode(vars1) + b'\n')

	xx = []
	for var in vars_:
		attrs = ds.attrs(d, var)
		x = ds.var(d, var)
		if opts.get('h') and \
		   attrs.get('units') == 'days since -4713-11-24 12:00 UTC' and \
		   attrs.get('calendar') == 'proleptic_gregorian':
			x = aq.to_iso(x)
		if x is None:
			x = np.array([])
		if not isinstance(x, np.ndarray) or x.ndim == 0:
			x = [x]
		xx += [x]
	n = len(xx[0])
	for i in range(n):
		y = [x[i] for x in xx]
		if len(y) == 1: y = y[0]
		sys.stdout.buffer.write(misc.encode(y) + b'\n')
