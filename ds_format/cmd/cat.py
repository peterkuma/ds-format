from ds_format.cmd import UsageError
import ds_format as ds
import aquarius_time as aq

def pretty(x, var):
	if var.get('units_comment') == 'julian_date(utc)':
		return aq.to_datetime(x).strftime('%Y-%m-%dT%H:%M:%S')
	return str(x)

def cat(*args, **opts):
	if len(args) < 1:
		raise TypeError('Usage: cat <var> <input>...')
	vars_ = args[0].split(',')
	input_ = args[1:]
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
