import pySpice.global_data
from pySpice.parser.parseline import *
from pySpice.parser.internalize import internalize
import pdb
def parser(netlist):
	"""
    Top-Level Encapsulation for Parsing Utilities

    :returns:
        + *element_DICT*: A dictionary containing the structure instance representing the circuit elements. With the element's name as index
        + *ANALYSIS_LIST*: List containing the instance for analysis comands
        + *SETTING_LIST*: List of instance for setting commands
        + *PRINT_DICT*: PRINT/PLOT command are parsed specially into special-designed structures, the instance of these structures are put into this dictionary. The dictionary has three items, with index of *dc*, *ac* and *tran* resepctively. Each item's value is a list of the print/plot instances

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
			if line[0] == '*' or line == '\n' or line == '\r\n':
				continue
			elif line[0] == '.':
				parse_ctrl(line)
			else:
				node_dim, branch_dim = parse_element(line,node_dim,branch_dim)

	internalize(node_dim)
	# 0 included
	pySpice.global_data.MNA_dim = node_dim + branch_dim
	
