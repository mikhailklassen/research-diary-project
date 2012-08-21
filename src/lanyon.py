#!/usr/bin/python
import os
import re
import yaml
import envoy
import markdown
import jinja2 as j2
from argparse import ArgumentParser

def fmt_entry_date(date):
	(year, month, day) = date.split('-')
	return ' %s $|$ %s $|$ %s' % (year, month, day)

def texify(md_string):
	r = envoy.run('pandoc -f markdown -t latex', data=md_string)
	return r.std_out

def build_tex(params, env, body):
	template = env.get_template('entry.tex')
	content = yaml.load(body)
	bodytex = texify(content['body'])
	try:
		os.mkdir('latex')
	except OSError:
		pass
	try:
		os.mkdir('pdf')
	except OSError:
		pass
	try:
		os.mkdir('build')
	except OSError:
		pass
	texfile = open('latex/'+content['date']+'.tex', 'w')
	texfile.write(template.render(entrydate=fmt_entry_date(content['date']), author=params['author'], institution=params['institution'], body=bodytex))
	texfile.close()
	envoy.run('cp src/research_diary.sty build/')
	envoy.run('cp latex/'+content['date']+'.tex build/')
	for img in os.listdir('images'): #Kludgey as FUUUUCK
		envoy.run('cp images/%s build/' % img)
	for command in params['latex_compiler']:
		envoy.run(re.sub('FILENAME', content['date'], command), cwd='build/')
	envoy.run('mv build/'+content['date']+'.pdf pdf/')
	envoy.run('rm -r build')
	r = envoy.run(params['pdf_viewer']+' pdf/'+content['date']+'.pdf')

def add(params, env, args):
	pass

def build(params, env, args):
	builders = {'latex':build_tex}
	try:
		if len(args.command) == 1:
			filename = 'entries/'+sorted(os.listdir('entries'))[-1]
		else:
			filename = args.command[1]
		body = open(filename).read()
	except:
		print "Unable to open entry!"
		exit(2)
	builders[args.format](params, env, body)
	pass

def book(params, env, args):
	pass

if __name__ == "__main__":
	commands = {'add':add, 'build':build, 'book':book}
	parser = ArgumentParser()
	parser.add_argument('command', nargs='+')
	parser.add_argument('-f', '--format', default='latex')
	args = parser.parse_args()
	try:
		params = yaml.load(open('params.yaml').read())
	except IOError:
		print "Unable to open parameter file: are you in the main lanyon directory?"
		exit(1)
	env = j2.Environment(loader=j2.FileSystemLoader('src/templates'))
	commands[args.command[0]](params, env, args)
