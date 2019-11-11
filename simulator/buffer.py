
from utils import clip


class Buffer:
	def __init__(self):
		self.pool = 0


	def add(self, demand):
		self.pool += demand


	def remove(self, demand):
		self.pool -= demand
		self.pool = clip(self.pool, 0, self.pool)


	def size(self):
		return self.pool


	def __repr__(self):
		return 'Buffer<{}>'.format(self.pool)