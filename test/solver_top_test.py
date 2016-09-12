from nose.tools import *
from pySpice.solver.stamp import *
from pySpice.solver.solver import *
from pySpice.solver.engine import *
from pySpice.parser.parser import *
import pySpice.global_data
import numpy as np

def test_single_solve():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'rlc.sp')
	assert_equal(len(pySpice.global_data.ANALYSIS_LIST),2)
	single_solve('ac',pySpice.global_data.ANALYSIS_LIST[0])

#if __name__ =='__main__':
