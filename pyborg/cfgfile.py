
import string

def load_config(filename):
	"""
	Load a config file returning dictionary of variables.
	"""
	try:
		f = open(filename, "r")
	except IOError, e:
		return None

	stuff = {}
	line = 0

	while 1:
		line = line + 1
		s = f.readline()
		if s=="":
			break
		if s[0]=="#":
			continue
		s = string.split(s, "=")
		if len(s) != 2:
			print "Malformed line in %s line %d" % (filename, line)
			continue
		stuff[string.strip(s[0])] = eval(string.strip(string.join(s[1:], "=")))

	return stuff
		
def save_config(filename, fields):
	"""
	fields should be a dictionary. Keys as names of
	variables containing tuple (string comment, value).
	"""
	f = open(filename, "w")

	# write the values with comments. this is a silly comment
	for key in fields.keys():
		f.write("# "+fields[key][0]+"\n")
		f.write(key+"\t= "+repr(fields[key][1])+"\n")
	f.close()


class cfgset:
	def load(self, filename, defaults):
		"""
		Defaults should be key=variable name, value=
		tuple of (comment, default value)
		"""
		self._defaults = defaults
		self._filename = filename

		for i in defaults.keys():
			self.__dict__[i] = defaults[i][1]

		# try to laad saved ones
		vars = load_config(filename)
		if vars == None:
			# none found. this is new
			self.save()
			return
		for i in vars.keys():
			self.__dict__[i] = vars[i]

	def save(self):
		"""
		Save borg settings
		"""
		keys = {}
		for i in self.__dict__.keys():
			# reserved
			if i == "_defaults" or i == "_filename":
				continue
			if self._defaults.has_key(i):
				comment = self._defaults[i][0]
			else:
				comment = ""
			keys[i] = (comment, self.__dict__[i])
		# save to config file
		save_config(self._filename, keys)

