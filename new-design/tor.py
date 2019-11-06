
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

	def _send_direct(self, dst_tor, capacity, buffers, msg):
		demand = buffers[dst_tor.id].size()
		to_send = clip(demand, 0, capacity)
		if to_send > 0:
			print("{} {} {}".format(msg, format_connection(self, dst_tor), to_send))
			buffers[dst_tor.id] -= to_send
			dst_tor.accept(to_send, )
		else:
			print("No {} for {}".format(msg, format_connection(self, dst_tor)))
		return to_send

	def accept(self, traffic, src_tor):
		print("Got {} from {}".format(traffic, src_tor))
		self.ingress_buffer.append((traffic, src_tor))

	def accept_indirect(self, traffic, indirector_tor, final_tor):
		print("Got {} to indirect to {} from {}".format(traffic, final_tor, src_tor))
		self.egress_non_local_buffers.add(traffic)

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
			self.egress_local_buffers[final_dst_tor.id] -= to_send
			print("Indirecting {} from {} via {}".format(to_send, format_connection(self, final_dst_tor), intermediate_tor))
			intermediate_tor.accept_indirect(to_send, src_tor, final_dst_tor)
		else:
			print("Not indirecting {} via {}".format(format_connection(self, final_dst_tor), intermediate_tor))
		return to_send


	def __repr__(self):
		return 'ToR<{}>'.format(self.tor_id)