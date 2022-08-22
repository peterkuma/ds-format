#!/usr/bin/env python
import os
import sys
import pst
import ds_format as ds
from ds_format import help
from ds_format.cmd import UsageError

def main():
	'''
	title: ds
	caption: "Tool for reading, writing and modifying dataset files."
	usage: {
		"`ds` [*cmd* [*args*]] [*options*]"
		"`ds --help` [*cmd*]"
		"`ds --version`"
	}
	arguments: {{
		*cmd*: "Command to execute or show help for. If omitted, `ds` is a shorthand for the command `ls`, with a difference that files with the same name as any available command cannot be listed. Available commands are listed below."
		*args*: "Command arguments and options."
	}}
	options: {{
		`-F`: "Interpret variable, dimension and attribute names as fixed strings, not glob patterns."
		`--help`: "Show this help message or help for a command."
		`--version`: "Print the version number and exit."
	}}
	desc: "The command line interface is based on the [PST format](https://github.com/peterkuma/pst). In all commands, variable, dimension and attribute names are interpreted as [glob patterns](https://docs.python.org/3/library/fnmatch.html), unless the `-F` option is enabled. Note that the pattern has to be enclosed in quotes in order to prevent the shell from interpreting the glob."
	"Available commands": {{
		`attrs`: "Print attributes in a dataset."
		`cat`: "Print variable data."
		`dims`: "Print dimensions of a dataset or a variable."
		`ls`: "List variables."
		`merge`: "Merge files along a dimension."
		`meta`: "Print dataset metadata."
		`rename`: "Rename variables and attributes."
		`rename_dim`: "Rename a dimension."
		`rm`: "Remove variables or attributes."
		`select`: "Select and subset variables."
		`set`: "Set variable data, dimensions and attributes in an existing or new dataset."
		`stats`: "Print variable statistics."
	}}
	"Supported input formats": {{
		NetCDF4: "`.nc`, `.nc4`, `.nc3`, `.netcdf`, `.hdf`, `.h5`"
		JSON: `.json`
	}}
	"Supported output formats": {{
		NetCDF4: "`.nc`, `.nc4`, `.netcdf`"
		JSON: `.json`
	}}
	author: "Written by Peter Kuma."
	copyright: "Copyright (c) 2019-2022 Peter Kuma. This software is distributed under an MIT license."
	'''
	a = pst.decode([os.fsencode(y) for y in sys.argv[1:]], as_unicode=True)
	args = []
	opts = {}
	if type(a) is list:
		if len(a) > 0 and type(a[-1]) is dict:
			opts = a[-1]
			a = a[:-1]
		if len(a) > 0 and type(a[0]) is dict:
			opts = a[0]
			a = a[1:]
		args = a
	elif type(a) is dict:
		opts = a
	elif a is not None:
		args = [a]

	if opts.get('help'):
		if len(args) == 1:
			cmd = args[0]
			f = ds.cmd.CMDS.get(cmd)
			if f is None:
				raise ValueError('Unknown command "%s"' % cmd)
			print(help.help_to_text(f.__doc__), end='')
		else:
			print(help.help_to_text(sys.modules[__name__].main.__doc__), end='')
		sys.exit(1)
	if opts.get('version'):
		print(ds.__version__)
		sys.exit(0)
	if len(args) == 0:
		sys.stderr.write('Usage: ds [CMD] [OPTIONS]\n')
		sys.stderr.write('       ds --help\n')
		sys.stderr.write('       ds --version\n')
		sys.stderr.write('Use `ds --help` for help.\n')
		sys.exit(1)
	cmd = args[0]
	cmd_args = args[1:]
	f = ds.cmd.CMDS.get(cmd)
	if f is None:
		cmd = 'ls'
		cmd_args = args
		f = ds.cmd.CMDS.get(cmd)
	if f is None:
		sys.stderr.write('%s: no such command\n' % cmd)
		sys.exit(1)
	if not getattr(f, 'disable_cmd_opts', False):
		opts.update({k: v for x in cmd_args if type(x) is dict \
			for k, v in x.items()})
		cmd_args = [x for x in cmd_args if type(x) is not dict]
	try:
		f(*cmd_args, **opts)
	except IOError as e:
		print(e)
		sys.exit(1)
	except UsageError as e:
		print('%s' % e, file=sys.stderr)
		print(help.help_to_usage(f.__doc__), end='', file=sys.stderr)
		print('Use `ds %s --help` for command help.' % cmd, file=sys.stderr)
