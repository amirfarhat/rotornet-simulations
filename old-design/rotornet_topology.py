
from rotornet_tor import ToR
from rotor_switch import RotorSwitch


def _make_matchings(num_tors):
	matchings = []
	for shift in range(1, num_tors):
	    # match i to i + shift with loopback
	    matching = [(src_tor, (src_tor+shift) % num_tors) for src_tor in range(num_tors)]
	    matchings.append(matching)
	return matchings

def _distribute_matchings(matchings, num_tors, num_rotor_switches):
	num_matchings = num_tors - 1
	matchings_per_sw, leftovers = divmod(num_matchings, num_rotor_switches)
	rotor_switches = [[] for _ in range(num_rotor_switches)]
	# deal with the quotient
	m = 0
	for r in range(num_rotor_switches):
	    for _ in range(matchings_per_sw):
	        rotor_switches[r].append(matchings[m])
	        m += 1
	# deal with the remainder
	for r in range(leftovers):
	    rotor_switches[r].append(matchings[m])
	    m += 1
	return rotor_switches


class RotorNetTopology:
	def __init__(self,
				 num_tors,
				 num_rotor_switches,
				 link_capacity
	 ):
		self.num_tors = num_tors
		self.num_rotor_switches = num_rotor_switches
		self.link_capacity = link_capacity

		self.tors = [ ToR(i) for i in range(num_tors) ]

		self.matchings = _make_matchings(num_tors)
		self.rotor_switches = _distribute_matchings(self.matchings, num_tors, num_rotor_switches)

	@property
	def formatted_matchings(self):
		out = []
		for r, rsw in enumerate(self.rotor_switches):
			for m in rsw:
				for src, dst in m:
					out.append('{} ~> {} on rotor {}'.format(src, dst, r))
		return '\n'.join(out)

	def neighbors_of_tor(self, tor, slot):
		neighbors = []
		for r, rsw in enumerate(self.rotor_switches):
			matching = rsw[slot % len(rsw)]
			for src, dst in matching:
				if src == tor.id:
					neighbors.append(self.tors[dst])
		return neighbors




