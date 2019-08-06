from .misc import UsageError, NumpyEncoder

from .merge import merge
from .info import info
from .ls import ls
from .cat import cat
from .stats import stats
#from .dims import dims
from .get import get
from .select import select

CMDS = {
	'merge': merge,
	'info': info,
	'ls': ls,
	'cat': cat,
	'stats': stats,
	'get': get,
	'select': select,
#	'dims': dims,
}
