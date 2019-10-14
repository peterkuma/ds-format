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
