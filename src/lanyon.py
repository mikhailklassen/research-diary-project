#!/usr/bin/python
import jinja2 as j2
import yaml
import envoy
import markdown
from argparse import ArgumentParser

def build_tex(params, body):

def build_html(params, body):

if __name__ == "__main__"
	parser = ArgumentParser()
	(options, args) = parser.parse_args()
	if len(args) < 1:
		print "Insufficient arguments:  use --help for more info."
		exit(1)
	try:
		params = yaml.load(open('params.yaml').readlines())
	except IOError:
		print "Unable to open parameter file: are you in the main lanyon directory?"
