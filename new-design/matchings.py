
from tor import ToR

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


class Matchings:
    def __init__(self, tors, rotors):
        self.tors = tors
        self.rotors = rotors

        self.matchings = self._make_matchings()

    @classmethod
    def generate(cls, tors, rotors):
        matchings = Matchings(tors, rotors)
        return _distribute_matchings(matchings.matchings, len(tors), len(rotors))

    def _make_matchings(self):
        matchings = []
        for shift in range(1, len(self.tors)):
            matching = []
            for i, src_tor in enumerate(self.tors):
                # match tor (i) to tor (i + shift) without self-links
                dst_tor = self.tors[(i + shift) % len(self.tors)]
                matching.append((src_tor, dst_tor))
            matchings.append(matching)
        return matchings