import pst
from markdown import markdown
from bs4 import BeautifulSoup

def f(s):
	soup = BeautifulSoup(markdown(s), features='lxml')
	for e in soup.find_all('em'):
		if e.string is not None:
			e.string = e.string.upper()
	return soup.get_text()

def help_to_usage(x):
	d = pst.decode(x.encode('utf-8'), as_unicode=True)
	s = ''
	if 'usage' in d:
		s += 'Usage: '
		if type(d['usage']) is list:
			for i, line in enumerate(d['usage']):
				if i > 0: s += '       '
				s += '%s\n' % f(line)
		else:
			s += '%s\n' % f(d['usage'])
	return s

def help_to_text(x):
	def to_list(label, items):
		s = ''
		s += '\n%s:\n\n' % label
		n = max([len(f(k)) for k in items.keys()])
		for k, v in items.items():
			s += ('  %-' + str(n) + 's  %s') % (f(k), f(v)) + '\n'
		return s
	d = pst.decode(x.encode('utf-8'), as_unicode=True)
	s = ''
	if 'title' in d and 'caption' in d:
		s += '%s: %s\n' % (d['title'], d['caption'])
	elif 'title' in d:
		s += '%s\n' % d['title']
	elif 'caption' in d:
		s += '%s\n' % d['caption']
	if 'usage' in d:
		s += '\nUsage: '
		if type(d['usage']) is list:
			for i, line in enumerate(d['usage']):
				if i > 0: s += '       '
				s += '%s\n' % f(line)
		else:
			s += '%s\n' % f(d['usage'])
	if 'desc' in d:
		s += '\n%s\n' % f(d['desc'])
	if 'arguments' in d:
		s += to_list('Arguments', d['arguments'])
	if 'options' in d:
		s += to_list('Options', d['options'])
	for k, v in d.items():
		if k in ['title', 'usage', 'desc', 'arguments', 'options', 'examples', 'environment', 'footer']:
			continue
		if type(v) is not dict:
			continue
		s += to_list(k, v)
	if 'examples' in d:
		s += '\nExamples:\n'
		for k, v in d['examples'].items():
			s += '\n%s\n\n' % k
			for line in v.split('\n'):
				s += '  %s\n' % line
	if 'environment' in d:
		s += to_list('Environment variables', d['environment'])
	if 'footer' in d:
		s += '\n%s\n' % d['footer']
	return s

def help_to_md(x):
	def to_list(label, items, code=False):
		s = ''
		s += '\n%s:\n\n' % label
		n = max([len(k) for k in items.keys()])
		for k, v in items.items():
			s += ('- %s: %s') % (k, v) + '\n'
		return s
	d = pst.decode(x.encode('utf-8'), as_unicode=True)
	s = ''
	if 'title' in d:
		s += '#### %s\n' % d['title']
	if 'aliases' in d:
		s += '\nAliases: '
		for alias in d['aliases']:
			s += ' %s' % alias
		s += '\n\n'
	if 'caption' in d:
		s += '\n%s\n' % d['caption']
	if 'usage' in d:
		s += '\nUsage: '
		if type(d['usage']) is list:
			s += '\n\n'
			for i, line in enumerate(d['usage']):
				s += '%s<br />\n' % line
			s += '\n'
		else:
			s += '%s\n' % d['usage']
	if 'desc' in d:
		s += '\n' + d['desc'] + '\n'
	if 'arguments' in d:
		s += to_list('Arguments', d['arguments'], True)
	if 'options' in d:
		s += to_list('Options', d['options'], True)
	if 'returns' in d:
		s += '\nReturn value:\n\n%s\n' % d['returns']
	for k, v in d.items():
		if k in ['title', 'usage', 'desc', 'arguments', 'options', 'examples', 'environment', 'footer']:
			continue
		if type(v) is not dict:
			continue
		s += to_list(k, v, True)
	if 'environment' in d:
		s += to_list('Environment variables', d['environment'], True)
	if 'examples' in d:
		s += '\nExamples:\n'
		for k, v in d['examples'].items():
			s += '\n%s\n' % k
			s += '\n```\n%s\n```\n' % v
	return s

def help_to_ronn(x):
	def esc(s):
		return s.replace('<', '&lt;').replace('>', '&gt;')
	def to_list(label, items, code=False):
		s = ''
		s += '\n## %s\n\n' % label.upper()
		n = max([len(k) for k in items.keys()])
		for k, v in items.items():
			s += ('- %s:\n%s') % (k, v) + '\n'
		return s
	d = pst.decode(x.encode('utf-8'), as_unicode=True)
	s = ''
	if 'title' in d:
		line = ('%s(1)' if d['title'] == 'ds' else 'ds-%s(1)') % d['title']
		if 'caption' in d:
			line += ' -- %s' % d['caption']
		n = len(line)
		s += '%s\n' % line
		s += '='*n + '\n'
	if 'usage' in d:
		s += '\n## SYNOPSIS\n\n'
		if type(d['usage']) is list:
			for i, line in enumerate(d['usage']):
				s += '%s<br>\n' % line
		else:
			s += '%s\n' % d['usage']
	if 'desc' in d:
		s += '\n## DESCRIPTION\n'
		s += '\n%s\n' % d['desc']
	if 'arguments' in d:
		s += to_list('Arguments', d['arguments'], True)
	if 'options' in d:
		s += to_list('Options', d['options'], True)
	for k, v in d.items():
		if k in ['title', 'usage', 'desc', 'arguments', 'options', 'examples', 'environment', 'footer']:
			continue
		if type(v) is not dict:
			continue
		s += to_list(k, v, True)
	if 'examples' in d:
		s += '\n## EXAMPLES\n\n'
		if type(d['examples']) is dict:
			for k, v in d['examples'].items():
				s += '%s\n\n' % k
				for line in v.split('\n'):
					s += '    %s\n' % line
				s += '\n'
	if 'environment' in d:
		s += to_list('Environment', d['environment'], True)
	if 'author' in d:
		s += '\n## AUTHOR\n'
		s += '\n%s\n' % d['author']
	if 'copyright' in d:
		s += '\n## COPYRIGHT\n'
		s += '\n%s\n' % d['copyright']
	return s
