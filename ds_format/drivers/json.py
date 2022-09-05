import json
import numpy as np
import ds_format as ds
import datetime as dt
import aquarius_time as aq

READ_EXT = ['json']
WRITE_EXT = ['json']

def read(filename, variables=None, sel=None, full=False, jd=False):
	with open(filename) as f:
		d = json.load(f)
		for var in ds.vars(d):
			data = ds.var(d, var)
			if type(data) is list:
				ds.var(d, var, np.array(data))
	return d

def write(filename, d):
	d2 = ds.copy(d)
	for var in ds.vars(d2):
		var_e = ds.escape(var)
		data = ds.var(d2, var)
		if isinstance(data, np.ndarray):
			d2[var_e] = data.tolist()
	with open(filename, 'w') as f:
		json.dump(d2, f)

from_json = read
to_json = write
