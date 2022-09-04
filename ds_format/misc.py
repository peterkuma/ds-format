import numpy as np

def sel_slice(sel, dims):
	return tuple([
		slice(None) if dim not in sel.keys() else sel[dim]
		for dim in dims
	])

def sel_dims(sel, dims):
	return [
		dim
		for dim in dims
		if dim not in sel.keys() or \
			isinstance(sel[dim], np.ndarray) or \
			type(sel[dim]) in (list, tuple)
	]

def encoder(x):
	if isinstance(x, np.generic):
		return x.item()
	elif isinstance(x, np.ma.MaskedArray) or \
		isinstance(x, np.ma.core.MaskedConstant):
		return x.tolist(None)
	elif isinstance(x, np.ndarray):
		return x.tolist()
	else:
		return x
