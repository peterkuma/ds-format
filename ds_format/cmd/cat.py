from ds_format.cmd import UsageError
import ds_format as ds
import aquarius_time as aq

def pretty(x, var):
	if var.get('units') == 'days since -4713-11-24 12:00 UTC' and \
	   var.get('calendar') == 'proleptic_gregorian':
		return aq.to_iso(x)
	return str(x)

def cat(vars_, *input_, **opts):
	'''
	title: "cat"
	caption: "Print variable."
	usage: {
		"`ds cat` [*options*] *var* *input*"
		"`ds cat` [*options*] `{` *var*... `}` *input*"
	}
	arguments: {{
		*var*: "Variable name."
		*input*: "Input file."
	}}
	options: {{
		`-h`: "Print human-readable values."
		`--jd`: "Convert time variables to Julian dates (see [Aquarius Time](https://github.com/peterkuma/aquarius-time))."
	}}
	examples: {{
"Print temperature values in dataset.nc.":
"$ ds cat temperature dataset.nc
16.0
18.0
21.0"

"Print time and temperature values in dataset.nc.":
"$ ds cat { time temperature } dataset.nc
1,16.0
2,18.0
3,21.0
4,23.0
5,25.0
6,28.0"
	}}
	'''
	if not isinstance(vars_, list):
		vars_ = [vars_]
	for filename in input_:
		d = ds.read(filename, vars_,
			full=False,
			jd=(opts.get('jd') or opts.get('h')),
		)
		varsx = [x for x in d.keys() if not x.startswith('.')]
		if len(varsx) == 0:
			return
		dims0 = d['.'][varsx[0]]['.dims']
		for var in varsx:
			dims = d['.'][var]['.dims']
			if dims != dims0:
				raise ValueError('incompatible dimensions')
		n = d[vars_[0]].flatten().shape[0]
		for i in range(n):
			if opts.get('h'):
				s = ','.join([pretty(d[var].flatten()[i], d['.'][var]) for var in vars_])
			else:
				s = ','.join([str(d[var].flatten()[i]) for var in vars_])
			print(s)
