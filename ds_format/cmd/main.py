#!/usr/bin/env python
import os
import sys
import traceback
import pst
import ds_format as ds
from ds_format.help import help_to_text, help_to_usage
from ds_format.misc import UsageError
from ds_format.cmd import GLOBAL_OPTS, READ_OPTS, WRITE_OPTS

USAGE = '''Usage: ds [CMD] [OPTIONS]
	   ds --help
	   ds --version
Use `ds --help` for help.'''

def parse_args(argv):
	try:
		delim = argv.index('--')
	except ValueError:
		delim = len(argv)

	args = pst.decode([os.fsencode(y) for y in argv[:delim]], as_unicode=True)
	if args is None:
		args = []
	elif type(args) is not list:
		args = [args]
	args += argv[(delim+1):]

	cmd = None
	icmd = -1
	with_cmd_opts = True
	for i, arg in enumerate(args):
		func = ds.cmd.CMDS.get(arg) if type(arg) is str else None
		if func is not None:
			cmd = arg
			icmd = i
			with_cmd_opts = func.cmd_opts
			break

	cmd_args = []
	opts = {}
	for i, arg in enumerate(args):
		if i == icmd: pass
		elif (i < icmd or i == len(args) -1 or with_cmd_opts) and type(arg) is dict:
			opts.update(arg)
		else:
			cmd_args += [arg]

	return cmd, cmd_args, opts

def fix_rw_opts(opts):
	def fix_k(k):
		if k == 'range':
			return 'range_'
		return k
	def fix_v(v):
		if type(v) is list and len(v) == 1:
			return v[0]
		elif type(v) is list and len(v) == 0:
			return {}
		return v
	return {fix_k(k): fix_v(v) for k, v in opts.items()}

def main():
	r'''
	title: ds
	caption: "Tool for reading, writing and modifying dataset files."
	usage: {
		"`ds` [*cmd* [*args*]] [*options*] [*read_options*] [*write_options*]"
		"`ds --help` [*cmd*]"
		"`ds --version`"
	}
	arguments: {{
		*cmd*: "Command to execute or show help for. If omitted, `ds` is a shorthand for the command `ls`, with a difference that files with the same name as any available command cannot be listed. Available commands are listed below."
		*args*: "Command arguments and options."
	}}
	options: {{
		`-F`: "Interpret variable, dimension and attribute names as fixed strings instead of glob patterns."
		`--help`: "Show this help message or help for a command if *cmd* is supplied."
		`-j`: "Print command output as JSON instead of [PST](https://github.com/peterkuma/pst)."
		`-m`: "Moderate error handling mode. Report a warning on missing variables, dimensions and attributes. Overrides the DS_MODE environment variable."
		`--noindent`: "Disable output indentation."
		`-s`: "Strict error handling mode. Handle missing variables, dimensions and attributes as errors. Overrides the DS_MODE environment variable."
		`-t`: "Soft error handling mode. Ignore missing variables, dimensions and attributes. Overrides the DS_MODE environment variable."
		`-v`: "Be verbose. Print more detailed information and error messages."
		`--version`: "Print the version number and exit."
	}}
	desc: "The command line interface is based on the [PST format](https://github.com/peterkuma/pst). In all commands, variable, dimension and attribute names are interpreted as [glob patterns](https://docs.python.org/3/library/fnmatch.html), unless the `-F` option is enabled. Note that the pattern has to be enclosed in quotes in order to prevent the shell from interpreting the glob."
	"Available commands": {{
		`attrs`: "Print attributes in a dataset."
		`cat`: "Print variable data."
		`dim`: "Print dimension size."
		`dims`: "Print dimensions of a dataset or a variable."
		`ls`: "List variables."
		`merge`: "Merge files along a dimension."
		`meta`: "Print dataset metadata."
		`rename`: "Rename variables and attributes."
		`rename_dim`: "Rename a dimension."
		`rm`: "Remove variables or attributes."
		`select`: "Select and subset variables."
		`set`: "Set variable data, dimensions and attributes in an existing or new dataset."
		`size`: "Print variable size."
		`stats`: "Print variable statistics."
		`type`: "Print variable type."
	}}
	"Supported input formats": {{
		CSV/TSV: "`.csv`, `.tsv`, `.tab`"
		DS: `.ds`
		HDF5: "`.h5`, `.hdf5`, `.hdf`"
		JSON: `.json`
		NetCDF4: "`.nc`, `.nc4`, `.nc3`, `.netcdf`"
	}}
	"Supported output formats": {{
		CSV/TSV: "`.csv`, `.tsv`, `.tab`"
		DS: `.ds`
		HDF5: "`.h5`, `.hdf5`, `.hdf`"
		JSON: `.json`
		NetCDF4: "`.nc`, `.nc4`, `.netcdf`"
	}}
	"Read options": {{
		"`at:` *selector*": "At selector as `{` *var*`:` *value* ... `}` or `{` *var*`:` `{` *value*... `}` ... `}`, where *value* is the value of the variable *var* to select. The dimension indexes corresponding the variable are constrained so that a variable value closest to the value is selected."
		"`between:` *selector*": "Between selector as `{` *var*`: {` *start* *end* `}` ... `}`, where *start* is the start value of the variable *var*, and *end* is the end value. The dimension indexes corresponding to the variable are constrained so that variable values in the range are selected. If the value is `none`, the range start or end is unlimited. The range start is inclusive (closed), and the end is exclusive (open)."
		"`range:` *selector*": "Range selector as `{` *dim*`: {` *start* *end* `}` ... `}`, where *start* is the start index of the dimension *dim*, and *end* is the end index. If the index is `none`, the range is from the start or to the end of the dimension, respectively. Negative index values are counted from the end of the dimension. The range start is inclusive (closed), and the end is exclusive (open)."
		"`sel:` *selector*": "Selector as *dim*`:` *idx* pairs, where *dim* is a dimension name and *idx* is an index or a list of indexes as `{` *i*... `}`."
	}}
	"Write options": {{
		"`calendar:` *value*": "CF-Conventions calendar to use for time variables when writing NetCDF4 and HDF5 files."
		"`time_units:` *value*": "CF-Conventions units to use for time variables when writing NetCDF4 and HDF5 files."
	}}
	environment: {{
		DS_MODE: "Error handling mode. If \"strict\", handle missing variables, dimensions and attributes as errors. If \"moderate\", report a warning. If \"soft\", ignore missing items."
	}}
	author: "Written by Peter Kuma."
	copyright: "Copyright (c) 2019-2026 Peter Kuma. This software is distributed under an MIT license."
	'''
	cmd, cmd_args, opts = parse_args(sys.argv[1:])
	sys.exit(main2(cmd, *cmd_args, **opts))

def main2(cmd, *cmd_args,
	help=False,
	version=False,
	t=False,
	m=False,
	s=False,
	j=False,
	noindent=False,
	v=False,
	**opts,
):
	if help:
		if cmd is None:
			print(help_to_text(sys.modules[__name__].main.__doc__), end='')
		else:
			func = ds.cmd.CMDS[cmd]
			print(help_to_text(func.__doc__), end='')
		return 0

	if version:
		print(ds.__version__)
		return 0

	if t: ds.mode = 'soft'
	if m: ds.mode = 'moderate'
	if s: ds.mode = 'strict'
	if j: ds.output = 'json'
	ds.indent = not noindent

	if cmd is None and len(cmd_args) == 0:
		print(USAGE, file=sys.stderr)
		return 1
	elif cmd is None:
		cmd = 'ls'

	r = fix_rw_opts({k: v for k, v in opts.items() if k in READ_OPTS})
	w = fix_rw_opts({k: v for k, v in opts.items() if k in WRITE_OPTS})
	global_opts = {
		k: v for k, v in opts.items()
		if k not in (READ_OPTS + WRITE_OPTS)
	}

	func = ds.cmd.CMDS[cmd]
	try:
		func(*cmd_args, **global_opts, r=r, w=w)
	except UsageError as e:
		print(f'ds {cmd}: {e}', file=sys.stderr)
		print(help_to_usage(func.__doc__), end='', file=sys.stderr)
		print(f'Use `ds {cmd} --help` for command help.', file=sys.stderr)
		return 1
	except (IOError, NameError, ValueError, TypeError) as e:
		if v: traceback.print_exc()
		else: print(f'ds {cmd}: {e}', file=sys.stderr)
		return 1
	return 0
