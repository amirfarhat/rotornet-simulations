
from tor import ToR
from rotor import Rotor
from matchings import Matchings


class RotorNet:
	def __init__(self, num_tors, num_rotor_switches, link_capacity):
		self.num_tors = num_tors
		self.num_rotor_switches = num_rotor_switches
		self.link_capacity = link_capacity

		# create our ToRs
		self.tors = [ ToR(i, num_tors) for i in range(num_tors) ]

		# create our Rotors
		self.rotors = [ Rotor(i, self.tors, link_capacity) for i in range(num_rotor_switches) ]

	@property
	def num_slots(self):
		# count max number of slots, which is
		# up to 1 more than the number of matchings per rotor switch
		q, r = divmod(self.num_tors - 1, self.num_rotor_switches)
		return q + int(r != 0) 
	

	@property
	def distributed_matchings(self):
		return Matchings.generate(self.tors, self.rotors)
	