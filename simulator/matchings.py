
import math

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


def _make_matchings(tors):
        matchings = []
        for shift in range(1, len(tors)):
            matching = []
            for i, src_tor in enumerate(tors):
                # match tor (i) to tor (i + shift) without self-links
                dst_tor = tors[(i + shift) % len(tors)]
                matching.append((src_tor, dst_tor))
            matchings.append(matching)
        return matchings


def connectivity_matrix(matchings, num_tors):
    conn = [[0 for j in range(num_tors)] for i in range(num_tors)]
    for r, rsw in enumerate(matchings):
        for matching in rsw:
            for src, dst in matching:
                conn[src.id][dst.id] = 1
    return conn

class Matchings:
    def __init__(self, tors, rotors):
        self.tors = tors
        self.rotors = rotors


    @classmethod
    def generate_rotornet(cls, tors, rotors):
        matchings = _make_matchings(tors)
        return _distribute_matchings(matchings, len(tors), len(rotors))


    @classmethod
    def generate_fixed(cls, tors, rotors):
        matchings = _make_matchings(tors)
        matchings_per_rotor = math.ceil((len(tors) - 1) / len(rotors))
        out = []
        for r, _ in enumerate(rotors):
            rsw = [matchings[1] for _ in range(matchings_per_rotor)]
            out.append(rsw)
        return out