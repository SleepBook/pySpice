
def main():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'resistor.sp')
	sample = solve()
	format(sample, 'outprint.ls')
	plotter('outprint.ls')
	
	