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
		for var in ds.get_vars(d):
			if type(d[var]) is list:
				d[var] = np.array(d[var])
	return d

def write(filename, d):
	d2 = ds.copy(d)
	for var in ds.get_vars(d2):
		if isinstance(d2[var], np.ndarray):
			d2[var] = d2[var].tolist()
	with open(filename, 'w') as f:
		json.dump(d2, f)

from_json = read
to_json = write
