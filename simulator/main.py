
import click
import random
random.seed(123)

from rotornet import RotorNet
from matchings import connectivity_matrix
# from utils import connectivity_matrix

@click.command()
@click.option(
	'--results_file',
	type=str,
	default='results/runs.txt'
)
@click.option(
	'-t', 
	'--num_tors', 
	default = 3
)
@click.option(
	'-r', 
	'--num_rotor_switches', 
	default = 1
)
@click.option(
	'-c',
	'--link_capacity', 
	default = 1
)
def main(
	results_file,
	num_tors,
	num_rotor_switches,
	link_capacity,
):
	# make a rotornet simulator
	rotornet = RotorNet(num_tors, num_rotor_switches, link_capacity)

	# generate matchings
	matchings = rotornet.distributed_matchings('rotornet')
	print(connectivity_matrix(matchings, num_tors))

	# inject demand
	for i, tor_i in enumerate(rotornet.tors):
		for j, tor_j in enumerate(rotornet.tors):
			if i == j: continue
			rotornet.inject_direct_demand(tor_i, tor_j, 5 * random.random() * link_capacity)
			rotornet.inject_direct_demand(tor_j, tor_i, 5 * random.random() * link_capacity)
	# for i, src_tor in enumerate(rotornet.tors):
	# 	dst_tor = rotornet.tors[(i + 1) % len(rotornet.tors)]
	# 	rotornet.inject_direct_demand(src_tor, dst_tor, 4 * link_capacity)

	total_demand = rotornet.total_demand

	# begin running cycles
	# cycle = 0
	# while rotornet.total_demand > 0:
	# 	print('-----------Cycle: {}'.format(cycle))
	# 	print('Total demand: {}'.format(rotornet.total_demand))

	# 	for slot in range(rotornet.num_slots):
	# 		print('Slot: {}'.format(slot))

	# 		# install matching for this slot on the rotors
	# 		for r, rotor_matchings in enumerate(matchings):
	# 			matching = rotor_matchings[slot % len(rotor_matchings)]
	# 			rotornet.rotors[r].install_matching(matching)
	# 			print('{} matchings: {}'.format(rotornet.rotors[r], format_matching(rotornet.rotors[r].matching)))

	# 		# first: send second hop traffic
	# 		for rotor in rotornet.rotors:
	# 			rotor.send_second_hop_traffic()
	# 		print(rotornet.total_demand)

	# 		# second: send local traffic directly
	# 		for rotor in rotornet.rotors:
	# 			rotor.send_direct_traffic()
	# 		print(rotornet.total_demand)

	# 		# third: indirect traffic on leftover capacity
	# 		for rotor in rotornet.rotors:
	# 			rotor.send_indirectly()
	# 		print(rotornet.total_demand)
			

	# 	cycle += 1
		# print()

	# fname = '{}/run_tors{}_rotors{}_capacity{}.txt'.format(results_file, num_tors, num_rotor_switches, link_capacity)
	# with open(results_file, 'a') as runs:
	# 	runs.write('{},{}\n'.format(total_demand, cycle))

if __name__ == '__main__':
	main()