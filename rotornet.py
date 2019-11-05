
from rotornet_topology   import RotorNetTopology
from rotornet_demand     import RotorNetDemand
from utils               import clip

class RotorNet:
	def __init__(self, 
				 num_tors,
				 num_rotor_switches,
				 link_capacity
	 ):
		self.topology = RotorNetTopology(num_tors, num_rotor_switches, link_capacity)
		self.demand = RotorNetDemand(num_tors)

	def send_direct_traffic(self, src_tor, slot):
		# dst_tors connected to the given src_tor along with src <--> dst link capacities
		neighbor_tors = self.topology.neighbors_of_tor(src_tor, slot)
		capacities = { tor : self.topology.link_capacity for tor in neighbor_tors }

		# send non-local and local traffic directly to upcoming rack
		for dst_tor in neighbor_tors:

			# first priority: non-local traffic on its second hop
			nlt = self.demand.non_local(src_tor.id, dst_tor.id) # non-local traffic
			take = clip(nlt, 0, capacities[dst_tor])
			if take > 0:
				capacities[dst_tor] -= take
				print('Second-hop {:.2f} from {} to {}'.format(take, src_tor, dst_tor))
				self.demand.update_non_local(src_tor.id, dst_tor.id, nlt - take)
				# TODO record sending

			# second priority: local traffic
			# if capacities[dst_tor] > 0:
			lt = self.demand.local(src_tor.id, dst_tor.id) # local traffic
			take = clip(lt, 0, capacities[dst_tor])
			if take > 0:
				capacities[dst_tor] -= take
				print('Direct {:.2f} from {} to {}'.format(take, src_tor, dst_tor))
				self.demand.update_local(src_tor.id, dst_tor.id, lt - take)
				# TODO record sending

		return capacities
	
	def indirect_leftovers(self, src_tor, slot, leftover_capacities):
		# The amount of non-local traffic it can accept per destination is equal 
		# to the difference between amount of traffic that can be sent during 
		# one matching slot and the total queued local and non-local traffic
		neighbor_tors = self.topology.neighbors_of_tor(src_tor, slot)

		# offer indirect traffic through leftover capacity
		for dst_tor in neighbor_tors:
			demand = self.demand.local(src_tor.id, dst_tor.id)

			# if demand > 0:
			# 	remote_local = self.demand.local(src_tor.id, dst_tor.id)
			# 	remote_non_local = None
			# 	self.topology.link_capacity - ()

			if capacity > 0:
				indirect = clip(demand, 0, capacity) # indirect traffic				
				if indirect > 0:
					# remove indirect traffic from local demand
					print('Indirecting {:.2f} from {} to {}'.format(indirect, src_tor, dst_tor))
					self.demand.update_local(src_tor.id, dst_tor.id, demand - indirect)
					
					non_local = self.demand.non_local
					self.demand.update_non_local(src_tor.id, dst_tor.id, non_local - indirect)

	def run_slot(self, slot):
		# run rotorLB on the specified slot for each tor
		for src_tor in self.topology.tors:
			leftover_capacities = self.send_direct_traffic(src_tor, slot)
			self.indirect_leftovers(src_tor, slot, leftover_capacities)




