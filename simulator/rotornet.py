
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
	def local_demand(self):
		demand = [[None for j in range(self.num_tors)] for i in range(self.num_tors)]
		for i in range(self.num_tors):
			for j in range(self.num_tors):
				demand[i][j] = self.tors[i].egress_local_buffers[j].size()


	@property
	def non_local_demand(self):
		demand = [[None for j in range(self.num_tors)] for i in range(self.num_tors)]
		for i in range(self.num_tors):
			for j in range(self.num_tors):
				demand[i][j] = self.tors[i].egress_non_local_buffers[j].size()
	
	
	@property
	def total_demand(self):
		return sum(tor.total_demand for tor in self.tors)
	

	def distributed_matchings(self, matching_name):
		if matching_name == 'fixed':
			return Matchings.generate_fixed(self.tors, self.rotors)
		else:
			return Matchings.generate_rotornet(self.tors, self.rotors)


	def inject_direct_demand(self, src_tor, dst_tor, demand):
		src_tor.egress_local_buffers[dst_tor.id].add(demand)

	