class Timeline:
	def __init__(t):
		self.t = t
		self.statuses = []
		self.lastStatus = None


class Status:
	def __init__(status):
		self.text = status.get('text')