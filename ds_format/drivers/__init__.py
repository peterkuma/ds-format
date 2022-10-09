from . import csv
from . import ds
from . import hdf
from . import json
from . import netcdf

DRIVERS = {
	'csv': csv,
	'ds': ds,
	'hdf': hdf,
	'json': json,
	'netcdf': netcdf,
}
