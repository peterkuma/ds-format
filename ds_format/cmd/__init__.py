from .misc import UsageError, NumpyEncoder

from .attrs import attrs
from .cat import cat
from .dims import dims
from .set_dims import set_dims
from .get import get
from .ls import ls
from .merge import merge
from .meta import meta
from .rename import rename
from .rename_attr import rename_attr
from .rename_dim import rename_dim
from .rm import rm
from .rm_attr import rm_attr
from .select import select
from .set_ import set_
from .set_attrs import set_attrs
from .stats import stats
from .write import write

CMDS = {
	'attrs': attrs,
	'cat': cat,
	'dims': dims,
	'get': get,
	'ls': ls,
	'merge': merge,
	'meta': meta,
	'rename': rename,
	'rename_attr': rename_attr,
	'rename_dim': rename_dim,
	'rm': rm,
	'rm_attr': rm_attr,
	'select': select,
	'set': set_,
	'set_attrs': set_attrs,
	'set_dims': set_dims,
	'stats': stats,
	'write': write,
}
