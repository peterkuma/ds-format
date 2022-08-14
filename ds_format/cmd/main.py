#!/usr/bin/env python
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
		"`ds` [*cmd* [*args*]]"
		"`ds --help` [*cmd*]"
		"`ds --version`"
	}
	arguments: {{
		*cmd*: "Command to execute or show help for. If omitted, `ds` is a shorthand for the command `ls`, with a difference that files with the same name as any available command cannot be listed. Available commands are listed below."
		*args*: "Command arguments and options."
	}}
	options: {{
		`--help`: "Show this help message or help for a command."
		`--version`: "Print the version number and exit."
	}}
	desc: "The command line interface is based on the [PST format](https://github.com/peterkuma/pst)."
	"Available commands": {{
		`attrs`: "Print attributes in a dataset."
		`cat`: "Print variable data."
		`dims`: "Print dimensions of a dataset or a variable."
		`get`: "Get attribute at a path."
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
	author: "Written by Peter Kuma."
	copyright: "Copyright (c) 2019-2022 Peter Kuma. This software is distributed under an MIT license."
	'''
	args, opts = pst.decode_argv(sys.argv, as_unicode=True)
	if opts.get('help'):
		if len(args) == 2:
			cmd = args[1]
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
	if len(args) == 1:
		sys.stderr.write('Usage: ds [CMD] [OPTIONS]\n')
		sys.stderr.write('       ds --help\n')
		sys.stderr.write('       ds --version\n')
		sys.stderr.write('Use `ds --help` for help.\n')
		sys.exit(1)
	cmd = args[1]
	cmd_args = args[2:]
	f = ds.cmd.CMDS.get(cmd)
	if f is None:
		cmd = 'ls'
		cmd_args = args[1:]
		f = ds.cmd.CMDS.get(cmd)
	if f is None:
		sys.stderr.write('%s: no such command\n' % cmd)
		sys.exit(1)
	try:
		f(*cmd_args, **opts)
	except IOError as e:
		print(e)
		sys.exit(1)
	except UsageError as e:
		print('%s' % e, file=sys.stderr)
		print(help.help_to_usage(f.__doc__), end='', file=sys.stderr)
		print('Use `ds %s --help` for command help.' % cmd, file=sys.stderr)
