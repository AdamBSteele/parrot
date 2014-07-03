class Timeline:
	def __init__(t):
		self.t = t
		self.statuses = []
		self.lastStatus = None


class Status:
	def __init__(status):
		self.text = status.get('text')

def getSettings(filename):
	settings = {}
	for line in open(filename):
		x,y = line.split('=')
		settings[x.strip()] = y.strip()
	return settings

def getUserSettings(filename):
	settings = {}
	for line in open(filename):
		x,y = line.split('=')
		settings[x.strip()] = y.strip()
	return settings

def getTimeline(userSettings):
	pass 	