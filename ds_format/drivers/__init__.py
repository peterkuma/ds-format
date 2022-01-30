from . import netcdf
from . import json
from . import ds

DRIVERS = {
	'netcdf': netcdf,
	'json': json,
	'ds': ds,
}
