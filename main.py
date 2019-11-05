
import click

from rotornet import RotorNet

def report(rn, init=False):
	num_tors = rn.topology.num_tors
	num_rotor_switches = rn.topology.num_rotor_switches
	num_matchings = num_tors - 1
	matchings_per_rotor = num_matchings // num_rotor_switches

	if init:
		click.echo("Running with {} tors, {} rotors, {} matchings, {} matchings per rotor\n".format(\
						num_tors, num_rotor_switches, num_matchings, matchings_per_rotor))
		click.echo("Matchings\n{}\n".format(\
						rn.topology.formatted_matchings))
	click.echo("Demand\n{}\n".format(\
					rn.demand))


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
	# make the rotor network
	rn = RotorNet(num_tors, num_rotor_switches, link_capacity)

	# report on init
	report(rn, init=True)
	
	# determine maximum number of slots
	num_matchings = num_tors - 1 
	q, r = divmod(num_matchings, num_rotor_switches)
	num_slots = q + int(r != 0)

	# run cycles of simulation till no more demand
	cycle = 0
	while rn.demand.has_demand():
	# while cycle < 2:
		print('-----------Cycle: {}'.format(cycle))

		# run all matching slots
		for slot in range(num_slots):
			print('Slot: {}'.format(slot))
			rn.run_slot(slot)
			print()

		# report(rn)
		print()
		cycle += 1

	# report on finish
	report(rn)

if __name__ == '__main__':
	main()