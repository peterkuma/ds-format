#!/usr/bin/env python3
import signal
if hasattr(signal, 'SIGINT'):
	signal.signal(signal.SIGINT, signal.SIG_DFL)
if hasattr(signal, 'SIGPIPE'):
	signal.signal(signal.SIGPIPE, signal.SIG_DFL)
import warnings
warnings.simplefilter('ignore')
from ds_format.cmd.main import main
if __name__ == '__main__':
	main()
