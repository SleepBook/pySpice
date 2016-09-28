from pySpice.solver.stamp import *
from pySpice.solver.solver import *
from pySpice.solver.engine import *
from pySpice.parser.parser import *
from pySpice.exhibitor.formator import *
import pySpice.global_data

def solve_circuit(infile,outfile):
	reload(pySpice.global_data)
	parser(infile)
	sample = solve()
	format(sample, outfile)
	
