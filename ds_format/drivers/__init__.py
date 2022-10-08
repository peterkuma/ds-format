from . import ds
from . import hdf
from . import json
from . import netcdf

DRIVERS = {
	'ds': ds,
	'hdf': hdf,
	'json': json,
	'netcdf': netcdf,
}
