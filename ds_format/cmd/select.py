import ds_format as ds
from ds_format.cmd import UsageError

def select(input_, output, variables=None, sel=None):
	sel = sel[0] if sel is not None and len(sel) > 0 else None
	d = ds.read(input_, variables, sel)
	ds.write(output, d)
