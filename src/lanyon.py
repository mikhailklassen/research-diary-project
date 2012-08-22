#!/usr/bin/python
import os
import re
import yaml
import envoy
import markdown
import jinja2 as j2
from datetime import date
from argparse import ArgumentParser

def fmt_entry_date(date):
	return ' %4d $|$ %0d $|$ %2d' % (date.year, date.month, date.day)

def texify(md_string):
	r = envoy.run('pandoc -f markdown -t latex', data=md_string)
	return r.std_out

def texify_todo(todo):
	texstr = '\\section{To Do}\n\\begin{bullets}\n'
	for task in todo:
		texstr += '\\item'
		if task['status'] == 'done':
			texstr += '[\\checkmark]'
		if task['status'] == 'started':
			texstr += '[\\textleaf]'
		texstr += ' ' 
		texstr += task['task']
		texstr += '\n'
	texstr += '\\end{bullets}\n\n\\textleaf : \\textit{In Progress} \\qquad \\checkmark : \\textit{Completed}\n'
	return texstr

def build_tex(params, env, body):
	template = env.get_template('entry.tex')
	content = yaml.load(body)
	bodytex = ''
	if 'todo' in content:
		bodytex += texify_todo(content['todo'])
	bodytex += texify(content['body'])
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
	texfile = open('latex/'+str(content['date'])+'.tex', 'w')
	texfile.write(template.render(entrydate=fmt_entry_date(content['date']), author=params['author'], institution=params['institution'], body=bodytex))
	texfile.close()
	envoy.run('cp src/research_diary.sty build/')
	envoy.run('cp latex/'+str(content['date'])+'.tex build/')
	for img in os.listdir('images'): #Kludgey as FUUUUCK
		envoy.run('cp images/%s build/' % img)
	for command in params['latex_compiler']:
		envoy.run(re.sub('FILENAME', str(content['date']), command), cwd='build/')
	envoy.run('mv build/'+str(content['date'])+'.pdf pdf/')
	#envoy.run('rm -r build')
	r = envoy.run(params['pdf_viewer']+' pdf/'+str(content['date'])+'.pdf')

def add(params, env, args):
	today = date.today()
	if params['frequency'] == 'daily':
		entry_date = "%4d-%02d-%02d" % (today.year, today.month, today.day)
	elif params['frequency'] == 'monthly':
		entry_date = "%4d-%02d-%02d" % (today.year, today.month, 1)
	else:#Weekly
		entry_date = "%4d-%02d-%02d" % (today.year, today.month, today.day-today.weekday())
	if os.path.exists('entries/%s.md' % entry_date):
		print "File already exists, get to work editing it!"
		exit(3)
	else:
		entry_file = open('entries/%s.md' % entry_date, 'w')
		entry_file.write(yaml.dump({'date':entry_date}, default_flow_style=False))
		entry_file.write('body: |')
		entry_file.close()

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

def book(params, env, args):
	template = env.get_template('book.tex')
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
	if len(args.command) < 2:
		print "What year do you want to build the anthology for?"
		exit(4)
	entries = [i for i in sorted(os.listdir('entries/')) if i[:4] == args.command[1]]
	texfile = open('latex/anthology-%s.tex' % args.command[1], 'w')
	entries_yaml = []
	for entry in entries:
		content = yaml.load(open('entries/'+entry).read())
		content['body'] = texify(content['body'])
		content['date'] = fmt_entry_date(content['date'])
		entries_yaml.append(content)
	texfile.write(template.render(year=args.command[1], author=params['author'], institution=params['institution'], entries=entries_yaml))
	texfile.close()
	envoy.run('cp src/research_diary.sty build/')
	envoy.run('cp latex/anthology-%s.tex build/' % args.command[1])
	for img in os.listdir('images'): #Kludgey as FUUUUCK
		envoy.run('cp images/%s build/' % img)
	for command in params['latex_compiler']:
		envoy.run(re.sub('FILENAME', 'anthology-%s' % args.command[1], command), cwd='build/')
	envoy.run('mv build/anthology-%s.pdf pdf/' % args.command[1])
	envoy.run('rm -r build')
	r = envoy.run(params['pdf_viewer']+' pdf/anthology-%s.pdf' % args.command[1])

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
