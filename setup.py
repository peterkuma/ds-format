#!/usr/bin/env python

from setuptools import setup, find_packages
from glob import glob

setup(
	name='ds-format',
	version='4.1.0',
	entry_points={
		'console_scripts': ['ds = ds_format.bin.ds:main'],
	},
	packages=find_packages(),
	description='ds-format is an open source program, a Python package and a storage format which provides an interface for reading and writing NetCDF files, as well as its own data file format.',
	author='Peter Kuma',
	author_email='peter@peterkuma.net',
	keywords=['dataset', 'netcdf', 'hdf', 'json', 'numpy'],
	url='https://ds-format.peterkuma.net',
	platforms=['any'],
	python_requires='>=3.0',
	data_files=[
		('share/man/man1', glob('man/*.1')),
	],
	install_requires=[
		'numpy>=1.9.1',
		'scipy>=1.10.1',
		'netCDF4>=1.6.4',
		'cftime>=1.5.1',
		'pst-format>=1.2.0',
		'aquarius-time>=0.1.0',
		'beautifulsoup4>=4.9.3',
		'Markdown>=3.3.4',
		'h5py>=2.10.0',
		'lxml>=4.9.2',
	],
	license='MIT',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
	],
)
