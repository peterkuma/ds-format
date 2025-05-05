from .attrs import attrs
from .cat import cat
from .dim import dim
from .dims import dims
from .ls import ls
from .merge import merge
from .meta import meta
from .rename import rename
from .rename_dim import rename_dim
from .rm import rm
from .select import select
from .stats import stats
from .set_ import set_
from .size import size
from .type_ import type_

CMDS = {
	'attrs': attrs,
	'cat': cat,
	'dim': dim,
	'dims': dims,
	'ls': ls,
	'merge': merge,
	'meta': meta,
	'rename': rename,
	'rename_dim': rename_dim,
	'rm': rm,
	'select': select,
	'stats': stats,
	'set': set_,
	'size': size,
	'type': type_,
}
