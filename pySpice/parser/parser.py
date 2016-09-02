from pySpice.global_data import *
from pySpice.parser.parseline import parseline
from pySpice.parser.internalize import internalize

def parser(netlist):
	"""Parse Spice Netlist

	:returns element list: a list contain all the circuit conponent
	:returns analylist: a list contain the analysis cmds
	:returns setting list: list for setting objs
	:returns prints dic: a dict for print cmds, ac,dc,tran
	:raised KeyErr:
	"""
	
	node_dim = 1
	branch_dim = 0	
	parse_cursor = 1
	f = open(netlist)
	f.readline()

	for line in f.readlines():
		parse_cursor += 1
		if line.lower() == '.end':
			break
		else:
			if line[0] == '*':
				continue
			elif line[0] == '.':
				parse_ctrl(line)
			else:
				node_dim, branch_dim = parse_element(line,node_dim,branch_dim)

	internalize(node_dim)
	








