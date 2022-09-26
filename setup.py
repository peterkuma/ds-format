#!/usr/bin/env python

from setuptools import setup, find_packages
from glob import glob

setup(
	name='ds-format',
	version='2.0.1',
	scripts=['bin/ds'],
	packages=find_packages(),
	description='Python implementation of a dataset format DS for storing data along with metadata',
	author='Peter Kuma',
	author_email='peter@peterkuma.net',
	keywords=['dataset', 'netcdf', 'hdf', 'json', 'numpy'],
	url='https://github.com/peterkuma/ds-format',
	platforms=['any'],
	python_requires='>=3.0',
	data_files=[
		('man/man1', glob('man/*.1')),
	],
	install_requires=[
		'netCDF4',
		'cftime>=1.5.1',
		'pst-format>=1.2.0',
		'aquarius-time>=0.1.0',
		'beautifulsoup4>=4.9.3',
		'Markdown>=3.3.4',
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
