#!/usr/bin/env python
#
# PyBorg Offline line input module
#
# Copyright (c) 2000, 2001 Tom Morton
#

import string
import sys

import pyborg

class ModLineIn:
	"""
	Module to interface console input and output with the PyBorg learn
	and reply modules. Allows offline chat with PyBorg.
	"""
	# Command list for this module
	commandlist = "LineIn Module Commands:\n!quit"
	commanddict = { "quit": "Usage: !quit\nQuits pyborg and saves the dictionary" }

	def __init__(self, my_pyborg):
		self.pyborg = my_pyborg
		self.start()

	def start(self):
		print "PyBorg offline chat!\n"
		print "Type !quit to leave"
		while 1:
			try:
				body = raw_input("> ")
			except (KeyboardInterrupt, EOFError), e:
				print
				return
			if body == "":
				continue
			if body[0] == "!":
				if self.linein_commands(body):
					continue
			# Pass message to borg
			self.pyborg.process_msg(self, body, 100, 1, ( None ), owner = 1)

	def linein_commands(self, body):
		command_list = string.split(body)
		command_list[0] = string.lower(command_list[0])

		if command_list[0] == "!quit":
			sys.exit(0)

	def output(self, message, args):
		"""
		Output a line of text.
		"""
		print message

if __name__ == "__main__":
	# start the pyborg
	my_pyborg = pyborg.pyborg()
	try:
		ModLineIn(my_pyborg)
	except SystemExit:
		pass
	my_pyborg.save_all()
	del my_pyborg

