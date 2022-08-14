from .misc import UsageError, NumpyEncoder

from .attrs import attrs
from .cat import cat
from .dims import dims
from .get import get
from .ls import ls
from .merge import merge
from .meta import meta
from .rename import rename
from .rename_dim import rename_dim
from .rm import rm
from .select import select
from .stats import stats
from .set_ import set_

CMDS = {
	'attrs': attrs,
	'cat': cat,
	'dims': dims,
	'get': get,
	'ls': ls,
	'merge': merge,
	'meta': meta,
	'rename': rename,
	'rename_dim': rename_dim,
	'rm': rm,
	'select': select,
	'stats': stats,
	'set': set_,
}
