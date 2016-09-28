#from nose.tools import *
from pySpice.solver.stamp import *
from pySpice.solver.solver import *
from pySpice.solver.engine import *
from pySpice.parser.parser import *
from pySpice.exhibitor.formator import *
import pySpice.global_data
import numpy as np
import pdb

def test_single_solve():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'rc.sp')
	raw_output = single_solve(pySpice.global_data.ANALYSIS_LIST[0])
	#assert_equal(raw_output[0],0)

	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'rlc.sp')
	raw_output = single_solve(pySpice.global_data.ANALYSIS_LIST[0])
	print raw_output[0]

def test_solve_diode():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'diode.sp')
	raw_output = single_solve(pySpice.global_data.ANALYSIS_LIST[0])
	
def test_solve_rl():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'rl.sp')
	raw_output = solve()
	format(raw_output, 'testout.ls')

if __name__ =='__main__':
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	#parser(NETLIST_ROOT + 'pmos.sp')
	parser(NETLIST_ROOT + 'cmos_inverter.sp')
	raw_output = solve()
	format(raw_output, 'testout.ls')

	

