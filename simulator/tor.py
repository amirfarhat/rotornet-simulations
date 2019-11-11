
from buffer import Buffer
from utils import format_connection
from utils import clip


class ToR:
	def __init__(self, tor_id, num_tors):
		self.num_tors = num_tors
		self.ingress_buffer = []
		self.egress_local_buffers = [ Buffer() for _ in range(self.num_tors) ]
		self.egress_non_local_buffers = [ Buffer() for _ in range(self.num_tors) ]
		self.tor_id = tor_id


	@property
	def id(self):
		return self.tor_id


	@property
	def total_demand(self):
		local_demand = sum(map(lambda b: b.size(), self.egress_local_buffers))
		non_local_demand = sum(map(lambda b: b.size(), self.egress_non_local_buffers))
		return local_demand + non_local_demand


	def _send_direct(self, dst_tor, capacity, buffers, msg):
		demand = buffers[dst_tor.id].size()
		to_send = clip(demand, 0, capacity)
		if to_send > 0:
			print("{} {} thru {}".format(msg, to_send, format_connection(self, dst_tor)))
			buffers[dst_tor.id].remove(to_send)
			dst_tor.accept(to_send, self)
		else:
			print("No {} for {}".format(msg, format_connection(self, dst_tor)))
			pass
		return to_send


	def accept(self, traffic, src_tor):
		print("Got {} from {}".format(traffic, src_tor))
		self.ingress_buffer.append((traffic, src_tor))


	def accept_indirect(self, traffic, indirector_tor, final_tor):
		print("Got {} to indirect to {} from {}".format(traffic, final_tor, indirector_tor))
		self.egress_non_local_buffers[final_tor.id].add(traffic)


	def send_second_hop(self, dst_tor, capacity):
		# use non-local demand on its second hop self --> dst_tor
		# to send directly to final destination
		return self._send_direct(dst_tor, capacity, self.egress_non_local_buffers, "second hopping")


	def send_direct(self, dst_tor, capacity):
		# use local/direct demand for self --> dst_tor
		# to send directly to final destination
		return self._send_direct(dst_tor, capacity, self.egress_local_buffers, "directing")


	def send_indirect(self, intermediate_tor, final_dst_tor, capacity):
		# use local/direct demand for self --> dst_tor
		# to indirect through the intermediate tor
		demand = self.egress_local_buffers[final_dst_tor.id].size()
		to_send = clip(demand, 0, capacity)
		if to_send > 0:
			self.egress_local_buffers[final_dst_tor.id].remove(to_send)
			print("Indirecting {} from {} via {}".format(to_send, format_connection(self, final_dst_tor), intermediate_tor))
			intermediate_tor.accept_indirect(to_send, self, final_dst_tor)
		else:
			print("Not indirecting {} via {}".format(format_connection(self, final_dst_tor), intermediate_tor))
			pass
		return to_send


	def __repr__(self):
		return 'ToR<{}>'.format(self.tor_id)