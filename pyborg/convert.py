#!/usr/bin/env python

#
# Use to convert pyborg 0.9.10 and 0.9.11 dictionaries to the
# version 1.0.0+ format.
#

import sys
import marshal
import struct
import string

# Read the dictionary
print "Reading dictionary stage 1..."

try:
	f = open("lines.dat", "r")
	s = f.read()
	f.close()
	lines = marshal.loads(s)
	del s
except (EOFError, IOError), e:
	print "Error reading dictionary."
	sys.exit()

print "working..."
for x in lines.keys():
	# clean up whitespace mess
	line = lines[x]
	words = string.split(line)
	lines[x] = string.join(words, " ")

print "Saving Dictionary..."

f = open("lines.dat", "w")
s = marshal.dumps(lines)
f.write(s)
f.close()

# Read the dictionary
print "Reading dictionary stage 2..."

try:
	f = open("words.dat", "r")
	s = f.read()
	f.close()
	words = marshal.loads(s)
	del s
except (EOFError, IOError), e:
	print "Error reading dictionary."
	sys.exit()

print "working..."
for key in words.keys():
	# marshallise it:
	y = []
	for i in words[key]:
		y.append(struct.pack("iH", i[0], i[1]))
	words[key] = y

print "Saving Dictionary..."

f = open("words.dat", "w")
s = marshal.dumps(words)
f.write(s)
f.close()
print "Done."

