from pySpice.solver.stamp import *
from pySpice.solver.solver import *
from pySpice.solver.engine import *
from pySpice.parser.parser import *
from pySpice.exhibitor.formator import *
import pySpice.global_data

def solve_circuit(infile,outfile):
	"""
	Top Encapsulation of the Program

	:param infile: string specify the netlist's name
	:param outfile: string specify the text report's name
	"""
	reload(pySpice.global_data)
	parser(infile)
	sample = solve()
	format(sample, outfile)
	
