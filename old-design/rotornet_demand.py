
import random
# random.seed(123)

def _make_matrix(n, filler_func = lambda : 10 * random.random()):
	out = []
	for i in range(n):
		row = []
		for j in range(n):
			if i == j:
				row.append(0)
			else:
				row.append(filler_func())
		out.append(row)
	return out

def _format_demand(src, dst, demand):
	return '{:.2f} demand for {} ~> {}'.format(demand, src, dst)

def _format_demand_matrix(matrix):
	out = []
	for src, row in enumerate(matrix):
		for dst, demand in enumerate(row):
			out.append(_format_demand(src, dst, demand))
	return '\n'.join(out)

class RotorNetDemand:
	def __init__(self, num_tors):
		self.num_tors = num_tors
		self.local_demand = _make_matrix(self.num_tors)
		self.non_local_demand = _make_matrix(self.num_tors, filler_func = lambda : 0)

	def has_demand(self):
		for matrix in [self.local_demand, self.non_local_demand]:
			for row in matrix:
				for value in row:
					if value != 0:
						return True
		return False

	def local(self, src, dst):
		return self.local_demand[src][dst]

	def format_local(self, src, dst):
		return _format_demand(src, dst, self.local(src, dst))

	def update_local(self, src, dst, new_value):
		self.local_demand[src][dst] = new_value

	def non_local(self, src, dst):
		return self.non_local_demand[src][dst]

	def format_non_local(self, src, dst):
		return _format_demand(src, dst, self.non_local(src, dst))

	def update_non_local(self, src, dst, new_value):
		self.non_local_demand[src][dst] = new_value

	def __str__(self):
		local = _format_demand_matrix(self.local_demand)
		non_local = _format_demand_matrix(self.non_local_demand)
		return 'Local\n{}\nNonLocal\n{}'.format(local, non_local)