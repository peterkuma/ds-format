from .misc import UsageError, NumpyEncoder

from .merge import merge
from .meta import meta
from .ls import ls
from .cat import cat
from .stats import stats
#from .dims import dims
from .get import get
from .select import select
from .write import write

CMDS = {
	'merge': merge,
	'meta': meta,
	'ls': ls,
	'cat': cat,
	'stats': stats,
	'get': get,
	'select': select,
	'write': write,
#	'dims': dims,
}
