#!/usr/bin/python
import jinja2 as j2
import yaml
import markdown
from argparse import ArgumentParser

if __name__ == "__main__"
	parser = ArgumentParser()
	(options, args) = parser.parse_args()
	if len(args) < 1:
		print "Insufficient arguments:  use --help for more info."
		exit(1)
