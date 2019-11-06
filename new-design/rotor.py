
class Rotor:
	def __init__(self, rotor_id, tors, link_capacity):
		self.matching = None
		self.rotor_id = rotor_id
		self.tors = tors
		self.link_capacity = link_capacity 
		self.links = None


	def _check_rep(self):
		if self.matching is None or self.links is None:
			raise Exception("No matching!!")


	def install_matching(self, new_matching):
		self.matching = list(new_matching)
		self.links = { (src.id, dst.id) : self.link_capacity for src, dst in self.matching }


	def send_second_hop_traffic(self):
		self._check_rep()
		# send traffic on its second hop in this matching
		for src_tor, dst_tor in self.matching:
			capacity = self.links[(src_tor.id, dst_tor.id)]
			sent = src_tor.send_second_hop(dst_tor, capacity)
			self.links[(src_tor.id, dst_tor.id)] -= sent


	def send_direct_traffic(self):
		self._check_rep()
		# send traffic directly from src to dst in this matching
		for src_tor, dst_tor in self.matching:
			capacity = self.links[(src_tor.id, dst_tor.id)]
			sent = src_tor.send_direct(dst_tor, capacity)
			self.links[(src_tor.id, dst_tor.id)] -= sent


	def send_indirectly(self):
		self._check_rep()

		# dst tor in matchings is now the intermediate tor
		for src_tor, int_tor in self.matching:

			# src tor forwards demand that will be satisfied in the next matching slot
			final_dst_tor = self.tors[(int_tor.id + 1) % len(self.tors)]
			capacity = self.links[(src_tor.id, int_tor.id)]
			sent = src_tor.send_indirect(int_tor, final_dst_tor, capacity)
			self.links[(src_tor.id, int_tor.id)] -= sent

	def __repr__(self):
		return 'Rotor<{}>'.format(self.rotor_id)