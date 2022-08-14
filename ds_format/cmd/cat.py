import numpy as np
from ds_format.cmd import UsageError
import ds_format as ds
from ds_format import misc
import aquarius_time as aq
import pst

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
	}}
	options: {{
		`-h`: "Print human-readable values (time as ISO 8601)."
		`--jd`: "Convert time variables to Julian date (see [Aquarius Time](https://github.com/peterkuma/aquarius-time))."
	}}
	desc: "Data are printed by the first index, one item per line, formatted as [PST](https://github.com/peterkuma/pst)-formatted. If multiple variables are selected, items at a given index from all variables are printed on the same line as an array."
	examples: {{
"Print temperature values in dataset.nc.":
"$ ds cat temperature dataset.nc
16.000000
18.000000
21.000000"

"Print time and temperature values in dataset.nc.":
"$ ds cat time temperature dataset.nc
1 16.000000
2 18.000000
3 21.000000"
	}}
	'''
	if len(args) < 1:
		raise UsageError('Invalid number of arguments')
	vars_ = args[:-1]
	input_ = args[-1]

	d = ds.read(input_, vars_,
		full=False,
		jd=(opts.get('jd') or opts.get('h')),
	)
	if len(vars_) == 0:
		return
	dims = [ds.get_dims(d, var) for var in vars_]
	if not all([dim == dims[0] for dim in dims]):
		raise ValueError('incompatible dimensions')

	xx = []
	for var in vars_:
		attrs = ds.get_attrs(d, var)
		x = d[var]
		if opts.get('h') and \
		   attrs.get('units') == 'days since -4713-11-24 12:00 UTC' and \
		   attrs.get('calendar') == 'proleptic_gregorian':
			x = aq.to_iso(x)
		if not isinstance(x, np.ndarray) or x.ndim == 0:
			x = [x]
		xx += [x]
	n = len(xx[0])
	for i in range(n):
		y = [x[i] for x in xx]
		print(pst.encode(y, encoder=misc.encoder).decode('utf-8'))
