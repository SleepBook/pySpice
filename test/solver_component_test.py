from nose.tools import *
from pySpice.solver.stamp import *
from pySpice.parser.parser import *
import pySpice.global_data
import numpy as np

def test_stamp_resistor():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'stamp1.sp')

	MNA = np.zeros((pySpice.global_data.MNA_dim, pySpice.global_data.MNA_dim))
	RHS = np.zeros((pySpice.global_data.MNA_dim,))
	sweep_flag, sweep_list, converge_flag, converge_list = stamp('dc', pySpice.global_data.ANALYSIS_LIST[0], MNA, RHS)
	
	assert_equal(sweep_flag, 1)
	assert_equal(sweep_list[0].switch, 'gen')
	assert_equal(sweep_list[0].coord, [((3,),1)])
	#assert_equal(RHS,[])
	#assert_equal(MNA,[])
	assert_equal(converge_flag, 0)

def test_stamp_xcxs():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'stamp2.sp')

	MNA = np.zeros((pySpice.global_data.MNA_dim, pySpice.global_data.MNA_dim))
	RHS = np.zeros((pySpice.global_data.MNA_dim,))
	sweep_flag, sweep_list, converge_flag, converge_list = stamp('dc', pySpice.global_data.ANALYSIS_LIST[0], MNA, RHS)

	assert_equal(sweep_flag, 1)
	assert_equal(sweep_list[0].switch, 'gen')
	assert_equal(sweep_list[0].coord, [((3,),1)])
	assert_equal(pySpice.global_data.NODE_TRANSLATION,{'1': 1, '0': 0, '2': 2, 'vin': 3, 'e1': 4})
	#assert_equal(MNA, [])
	#assert_equal(RHS, [])

def test_stamp_active():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'stamp3.sp')

	MNA = np.zeros((pySpice.global_data.MNA_dim, pySpice.global_data.MNA_dim))
	RHS = np.zeros((pySpice.global_data.MNA_dim,))
	sweep_flag, sweep_list, converge_flag, converge_list = stamp('ac', pySpice.global_data.ANALYSIS_LIST[0], MNA, RHS)

	assert_equal(sweep_flag, 1)
	assert_equal(sweep_list[0].switch, 'gen')
	#assert_equal(sweep_list[0].coord, [])
	assert_equal(sweep_list[1].switch, 'gen')
	#assert_equal(sweep_list[1].coord,[])

	MNA = np.zeros((pySpice.global_data.MNA_dim, pySpice.global_data.MNA_dim))
	RHS = np.zeros((pySpice.global_data.MNA_dim,))
	sweep_flag, sweep_list, converge_flag, converge_list = stamp('tran', pySpice.global_data.ANALYSIS_LIST[1], MNA, RHS)

	assert_equal(sweep_flag, 1)
	assert_equal(pySpice.global_data.NODE_TRANSLATION, {'1': 1, '0': 0, '2': 2, 'vin': 3, 'l1': 4})
	assert_equal(len(sweep_list), 3)
	assert_equal(sweep_list[0].switch, 'upd')
	#assert_equal(sweep_list[0].coord, [])
	assert_equal(sweep_list[2].switch, 'upd')
	#assert_equal(sweep_list[2].coord,[])
	assert_equal(sweep_list[1].switch,'gen')
	assert_equal(sweep_list[1].coord, [((3,),1)])

