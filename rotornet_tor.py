
class ToR:
	def __init__(self, tor_id):
		self.tor_id = tor_id

	@property
	def id(self):
		return self.tor_id
	
	def __repr__(self):
		return 'ToR<{}>'.format(self.tor_id)