#!/usr/bin/env python
#
# PyBorg ascii file input module
#
# Copyright (c) 2000, 2001 Tom Morton
#

import string
import sys

import pyborg

class ModFileIn:
	"""
	Module for file input. Learning from ASCII text files.
	"""

	# Command list for this module
	commandlist = "FileIn Module Commands:\nNone"
	commanddict = {}
	
	def __init__(self, Borg, args):

		f = open(args[1], "r")
		buffer = f.read()
		f.close()

		print "I knew "+`Borg.settings.num_words`+" words ("+`len(Borg.lines)`+" lines) before reading "+sys.argv[1]
		buffer = pyborg.filter_message(buffer)
		# Learn from input
		try:
			Borg.learn(buffer)
		except KeyboardInterrupt, e:
			# Close database cleanly
			print "Premature termination :-("
		print "I know "+`Borg.settings.num_words`+" words ("+`len(Borg.lines)`+" lines) now."
		del Borg

	def shutdown(self):
		pass

	def start(self):
		sys.exit()

	def output(self, message, args):
		pass

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Specify a filename."
		sys.exit()
	# start the pyborg
	my_pyborg = pyborg.pyborg()
	ModFileIn(my_pyborg, sys.argv)
	my_pyborg.save_all()
	del my_pyborg

