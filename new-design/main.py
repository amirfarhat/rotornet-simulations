
import click

from tor import ToR
from rotor import Rotor
from matchings import Matchings
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
	# create our ToRs
	tors = [ ToR(i, num_tors) for i in range(num_tors) ]
	
	# create our Rotors
	rotors = [ Rotor(i, tors, link_capacity) for i in range(num_rotor_switches) ]

	# generate matchings and distribute them across the rotors
	distributed_matchings = Matchings.generate(tors, rotors)

	# count max number of slots
	q, r = divmod(num_tors - 1, num_rotor_switches)
	num_slots = q + int(r != 0) 

	cycle = 0
	while cycle < 1:
		print('-----------Cycle: {}'.format(cycle))

		for slot in range(num_slots):
			print('Slot: {}'.format(slot))

			# install matching for this slot on the rotors
			for r, rotor_matchings in enumerate(distributed_matchings):
				matching = rotor_matchings[slot % len(rotor_matchings)]
				rotors[r].install_matching(matching)
				print('{} matchings: {}'.format(rotors[r], format_matching(rotors[r].matching)))

			# first: send second hop traffic
			for rotor in rotors:
				rotor.send_second_hop_traffic()

			# second: send local traffic directly
			for rotor in rotors:
				rotor.send_direct_traffic()

			# third: indirect traffic on leftover capacity
			for rotor in rotors:
				rotor.send_indirectly()
			

		cycle += 1
		print()

if __name__ == '__main__':
	main()