
class RotorSwitch:
	def __init__(self, rotor_id):
		self.rotor_id = rotor_id

	@property
	def id(self):
		return self.rotor_id
	
	def __repr__(self):
		return 'Rotor<{}>'.format(self.rotor_id)