
def format_connection(src_tor, dst_tor):
	return '{} ~> {}'.format(src_tor.id, dst_tor.id)

def format_matching(matching):
	return ', '.join(format_connection(src, dst) for src, dst in matching)

def clip(val, min_val, max_val):
	return max(min_val, min(val, max_val))