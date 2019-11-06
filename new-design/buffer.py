
class Buffer:
	def __init__(self):
		self.pool = 0

	def add(self, demand):
		self.pool += demand

	def size(self):
		return self.pool