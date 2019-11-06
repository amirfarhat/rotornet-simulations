
import click

from rotornet import RotorNet
from utils import format_matching

@click.command()
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
	'--link_capacity', 
	default = 1
)
def main(
	num_tors,
	num_rotor_switches,
	link_capacity,
):
	# make a rotornet simulator
	rotornet = RotorNet(num_tors, num_rotor_switches, link_capacity)
	
	# begin running cycles
	cycle = 0
	while cycle < 1:
		print('-----------Cycle: {}'.format(cycle))

		for slot in range(rotornet.num_slots):
			print('Slot: {}'.format(slot))

			# install matching for this slot on the rotors
			for r, rotor_matchings in enumerate(rotornet.distributed_matchings):
				matching = rotor_matchings[slot % len(rotor_matchings)]
				rotornet.rotors[r].install_matching(matching)
				print('{} matchings: {}'.format(rotornet.rotors[r], format_matching(rotornet.rotors[r].matching)))

			# first: send second hop traffic
			for rotor in rotornet.rotors:
				rotor.send_second_hop_traffic()

			# second: send local traffic directly
			for rotor in rotornet.rotors:
				rotor.send_direct_traffic()

			# third: indirect traffic on leftover capacity
			for rotor in rotornet.rotors:
				rotor.send_indirectly()
			

		cycle += 1
		print()

if __name__ == '__main__':
	main()