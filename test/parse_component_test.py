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

	ele2 = "VIN 2 0 0.01 AC 2 60 SIN(0 1 1X)"
	node_dim, branch_dim = parse_element(ele2, node_dim, branch_dim)
	assert_equal(node_dim,3)
	assert_equal(branch_dim, 1)
	assert_equal(ELEMENT_DICT['vin'].branch, 0)
	assert_equal(ELEMENT_DICT['vin'].branch_flag, 1)
	#assert_equal(ELEMENT_DICT['vin'].ac.real, 1.0)
	assert_equal(ELEMENT_DICT['vin'].ac.imag, 2 * math.sin(math.pi*60/180))
	assert_equal(ELEMENT_DICT['vin'].tran.freq, 1e06)

	ele3 = "E1 3 4 1 2 2.0"
	node_dim, branch_dim = parse_element(ele3, node_dim, branch_dim)
	assert_equal(node_dim, 5)
	assert_equal(branch_dim, 2)
	assert_equal(ELEMENT_DICT['e1'].branch, 1)
	assert_equal(ELEMENT_DICT['e1'].branch_flag, 1)
	assert_equal(ELEMENT_DICT['e1'].value, 2.0)

	ele4 = "F1 5 6 VIN 2.0"
	node_dim, branch_dim = parse_element(ele4, node_dim, branch_dim)
	assert_equal(node_dim, 7)
	assert_equal(branch_dim, 2)
	assert_equal(ELEMENT_DICT['f1'].loc_ctrl_branch, 0)
	assert_equal(ELEMENT_DICT['f1'].branch_flag, 1)

	ele5 = "G1 7 8  2 0 3.0"
	node_dim, branch_dim = parse_element(ele5, node_dim, branch_dim)
	assert_equal(node_dim, 9)
	assert_equal(branch_dim, 2)

	ele6 = "H1 9 10 VIN 3.0"
	node_dim, branch_dim = parse_element(ele6, node_dim, branch_dim)
	assert_equal(node_dim, 11)
	assert_equal(branch_dim, 3)
	assert_equal(ELEMENT_DICT['h1'].branch, 2)
	assert_equal(ELEMENT_DICT['h1'].loc_ctrl_branch, 0)
	assert_equal(ELEMENT_DICT['h1'].branch_flag, 1)

	ele7 = "M1 11 12 13 0 PMOS"
	node_dim, branch_dim = parse_element(ele7, node_dim, branch_dim)
	assert_equal(node_dim, 14)
	assert_equal(ELEMENT_DICT['m1'].name, 'm1')
	assert_equal(ELEMENT_DICT['m1'].model, 'pmos')
	assert_equal(ELEMENT_DICT['m1'].loc_d, 11)
	assert_equal(ELEMENT_DICT['m1'].loc_g, 12)
	assert_equal(ELEMENT_DICT['m1'].loc_s, 13)
	assert_equal(ELEMENT_DICT['m1'].loc_b, 0)

	ele8 = "M2 14 15 16 0 NMOS L=5u W=25u"
	node_dim, branch_dim = parse_element(ele8, node_dim, branch_dim)
	assert_equal(node_dim, 17)
	#assert_equal(ELEMENT_DICT['m2'].l, 5e-06)
	#assert_equal(ELEMENT_DICT['m2'].w, 25e-06)


	

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
	assert_equal(ANALYSIS_LIST[4].catagory, 'analy_tran')
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

	line3 = ".PRINT AC VM(4,2) VR(7) VP(8,3) IM(VSEC)"
	parse_ctrl(line3)
	assert_equal(PRINT_DICT['ac'][0].cmd, 'vm(4,2)')
	assert_equal(PRINT_DICT['ac'][0].op_flag, 1)
	assert_equal(PRINT_DICT['ac'][0].op_list, ['4','2'])

	assert_equal(PRINT_DICT['ac'][1].cmd, 'vr(7)')
	assert_equal(PRINT_DICT['ac'][2].cmd, 'vp(8,3)')
	assert_equal(PRINT_DICT['ac'][3].cmd, 'im(vsec)')


