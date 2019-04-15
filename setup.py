from setuptools import setup, find_packages

setup(
    name='ds-format',
    version='0.1.0',
    scripts=['bin/ds'],
    packages=find_packages(),
    description='DS: Dataset Format Python implementation',
    author='Peter Kuma',
    author_email='peter.kuma@fastmail.com',
    keywords=['netcdf', 'hdf'],
    url='https://github.com/peterkuma/ds-python',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
)
