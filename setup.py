#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='ds_format',
    version='0.1.0',
    scripts=['bin/ds'],
    packages=find_packages(),
    description='Python implementation of a dataset format DS for storing data along with metadata (in development)',
    author='Peter Kuma',
    author_email='peter.kuma@fastmail.com',
    keywords=['dataset', 'netcdf', 'hdf', 'json', 'numpy']
    url='https://github.com/peterkuma/ds-python',
    platforms=['any'],
    install_requires=['netCDF4'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
