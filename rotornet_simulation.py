
import random
random.seed(0)


# CONSTANTS ====================================================================

SCALE          = 1 # [0, 100]

N_R            = 4 # TOR COUNT
N_SW           = 2 # ROTOR SWITCH COUNT
MATCHING_COUNT = N_R - 1
CYCLES         = 5
LINK_CAPACITY  = 0.1 * SCALE # [capacity per slot]


# GLOBALS ======================================================================

# make matchings
matchings = []
for shift in range(1, N_R):
    # match i to i + shift with loopback
    matching = [(src_tor, (src_tor+shift) % N_R) for src_tor in range(N_R)]
    matchings.append(matching)

# distribute across rotor switches
matchings_per_sw, leftovers = divmod(MATCHING_COUNT, N_SW)
rotor_switches = [[] for _ in range(N_SW)]
# deal with the quotient
m = 0
for r in range(N_SW):
    for _ in range(matchings_per_sw):
        rotor_switches[r].append(matchings[m])
        m += 1
# deal with the remainder
for r in range(leftovers):
    rotor_switches[r].append(matchings[m])
    m += 1

# make demand
demand = [[random.random() * SCALE for j in range(N_R)] for i in range(N_R)]
for i in range(N_R):
    demand[i][i] = 0


# HELPERS ======================================================================

def print_demand():
    for src_tor, row in enumerate(demand):
        for dst_tor, d in enumerate(row):
            if src_tor != dst_tor:
                demand_statement = "{} --> {} demand: {}".format(src_tor, dst_tor, d)
                print(demand_statement)
    print()

def format_matching(m):
    return ', '.join(('{} ~> {}'.format(src, dst) for src, dst in m))

def print_matchings():
    # for slot, m in enumerate(matchings):
    #     matching_strs = ['{} ~> {}'.format(src, dst) for src, dst in m]
    #     print('Slot {}: {}'.format(slot + 1, ', '.join(matching_strs)))
    # print()
    for r, rsw in enumerate(rotor_switches):
        print('Rotor: {}'.format(r))
        for slot, m in enumerate(rsw):
            print('   Slot {}: {}'.format(slot + 1, format_matching(m)))
    print()

def print_rotor_switches():
    for _, r in enumerate(rotor_switches):
        print(r)
    print()


# MAIN =========================================================================

# print_matchings()
# print_demand()

# determine the number of slots
slots = 1
for r, rsw in enumerate(rotor_switches):
    slots = max(slots, len(rsw))

for cycle in range(CYCLES):
    print('Cycle: {}'.format(cycle + 1))

    for slot in range(slots):
        print('Slot: {}'.format(slot))

        for r, rsw in enumerate(rotor_switches):
            m = rsw[slot % len(rsw)]
            print('Rotor switch {} offers matching {}'.format(r, format_matching(m)))

            # send the link capacity in this slot for each matching
            for src, dst in m:
                d = demand[src][dst]
                to_send = min(d, LINK_CAPACITY)
                print('{} demand {:0.2f}, sending {} via rotor switch {}'.format(format_matching([(src, dst)]), d, to_send, r))
                demand[src][dst] -= to_send
            print()
        print()
    print()


    # for slot, m in enumerate(matchings):
    #     # print('Starting slot {}'.format(slot + 1))
    #     for src, dst in m:
    #         d = demand[src][dst]
    #         to_send = min(d, LINK_CAPACITY)
    #         # print('Demand {}, sending {} via {} ~> {}'.format(d, to_send, src, dst))
    #         demand[src][dst] -= to_send
    #     # print()
    
    

