from nose.tools import *
from pySpice.parser.parser import *
from pySpice.parser.parseline import *
from pySpice.global_data import *
from pySpice.parser.utils import *


def test_parse_timefunc():
	string1 = "sin(10 0 5x)"
	string2 = "sin 20k 5u 500"
	string3 = "pulse(2 0 2ns 2ns 2ns 50ns 100ns)"
	string4 = "pulse -1 1 2ns 3ns 3ms 50ns 100ns"

	item1 = parse_timefunc(string1)
	assert_equal(item1.catagory,"sin")
	assert_equal(item1.vdd,10)
	assert_equal(item1.vgnd,0)
	assert_equal(item1.freq,5e06)

	item2 = parse_timefunc(string2)
	assert_equal(item2.catagory, 'sin')
	assert_equal(item2.vdd, 2e04)
	#assert_equal(item2.vgnd, 5e-06)
	assert_equal(item2.freq, 500)

	item3 = parse_timefunc(string4)
	assert_equal(item3.catagory, 'pulse')
	assert_equal(item3.vdd, -1)
	assert_equal(item3.vgnd, 1)
	assert_equal(item3.td, 2e-09)
	assert_equal(item3.tf, 3e-03)

def test_parse_element():
	node_dim = 1
	branch_dim = 0
	assert_equal(len(ELEMENT_DICT),0)
	
	ele1 = "R1 1 0 30K"

	node_dim, branch_dim = parse_element(ele1, node_dim, branch_dim)
	assert_equal(node_dim,2)
	assert_equal(branch_dim, 0)
	assert_equal(ELEMENT_DICT['r1'].catagory,'r')
	assert_equal(ELEMENT_DICT['r1'].name,'r1')
	assert_equal(ELEMENT_DICT['r1'].value,3e04)
	assert_equal(ELEMENT_DICT['r1'].branch_flag,0)
	assert_equal(ELEMENT_DICT['r1'].active_flag,0)

	ele2 = "VIN 3 0 0.01 AC 1 35 SIN(0 1 1X)"
	node_dim, branch_dim = parse_element(ele2, node_dim, branch_dim)
	assert_equal(node_dim,3)
	assert_equal(branch_dim, 1)
	assert_equal(ELEMENT_DICT['vin'].branch, 0)
	assert_equal(ELEMENT_DICT['vin'].branch_flag, 1)
	assert_equal(ELEMENT_DICT['vin'].ac_mag, 1)
	assert_equal(ELEMENT_DICT['vin'].ac_phase, 35)
	assert_equal(ELEMENT_DICT['vin'].tran.freq, 1e06)

def test_linear_generator():
	start = 5
	stop = 10
	step = 1
	temp = 5
	for ex in linear_generator(start, stop, step):
		assert_equal(ex, temp)
		temp += 1

	start, stop = stop, start
	step = -1
	temp = 10
	for ex in linear_generator(start, stop, step):
		assert_equal(ex, temp)
		temp -= 1

def test_dec_generator():
	start = 1
	stop = 1000
	step = 3
	temp = 1
	factor = pow(10, 1./3)
	for ex in dec_generator(start, stop, step):
		assert_equal(ex, temp)
		temp *= factor

def test_oct_generator():
	start = 1
	stop = 4096
	step = 3
	temp = 1
	factor = pow(8, 1./3)
	for ex in oct_generator(start, stop, step):
		assert_equal(ex, temp)
		temp *= factor


def test_ctrl():
	line1 = ".op"
	
	parse_ctrl(line1)
	assert_equal(ANALYSIS_LIST[0],1)

	line2 = ".DC VIN 0.25 5.0 0.25"
	parse_ctrl(line2)
	assert_equal(ANALYSIS_LIST[1].swp_src, 'vin')
	for item1, item2 in zip(ANALYSIS_LIST[1].generator,linear_generator(0.25,5.0,0.25)):
		assert_equal(item1, item2)

	line3 = ".DC VIN 0.25 5.0 0.25 IB 0 10U 1U"
	parse_ctrl(line3)
	assert_equal(ANALYSIS_LIST[2].swp_src, 'vin')
	assert_equal(ANALYSIS_LIST[2].swp_src2,'ib')
	for item1,item2 in zip(ANALYSIS_LIST[2].generator2, linear_generator(0,extract('10u'),extract('1u'))):
		assert_equal(item1, item2)

	line4 = ".AC DEC 3 1 100K"
	parse_ctrl(line4)
	for item1, item2 in zip(ANALYSIS_LIST[3].generator, dec_generator(1, extract('100k'), 3)):
		assert_equal(item1, item2)

	line5 = ".TRAN 1NS 100NS"
	parse_ctrl(line5)
	assert_equal(ANALYSIS_LIST[4].catagory, 'tran')
	for item1, item2 in zip(ANALYSIS_LIST[4].generator, linear_generator(0,extract('100n'), extract('1n'))):
		assert_equal(item1, item2)

	line6 = ".TRAN 1NS 100NS UIC"
	parse_ctrl(line6)
	assert_equal(ANALYSIS_LIST[5].uic_flag, 1)
	
def test_parse_print():
	line1 = ".PRINT TRAN V(4) I(VIN)"
	assert_equal(PRINT_DICT['tran'],[])
	parse_ctrl(line1)	
	assert_equal(PRINT_DICT['tran'][0].cmd, 'v(4)')
	assert_equal(PRINT_DICT['tran'][0].op_flag, 0)
	assert_equal(PRINT_DICT['tran'][0].op_list, ['4'])	
	assert_equal(PRINT_DICT['tran'][1].cmd, 'i(vin)')

	line2 = ".PLOT DC V(4,3) I(VSEC)"
	parse_ctrl(line2)
	assert_equal(PRINT_DICT['dc'][0].cmd, 'v(4,3)')
	assert_equal(PRINT_DICT['dc'][0].op_flag, 1)
	assert_equal(PRINT_DICT['dc'][0].op_list,['4','3'])
	assert_equal(PRINT_DICT['dc'][1].op_flag, 0)
	assert_equal(PRINT_DICT['dc'][1].op_list, ['vsec'])

	
	
	








