from nose.tools import *
from pySpice.parser.parseline import *
from pySpice.global_data import *

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
	assert_equal(len(ELEMENT_LIST),0)
	
	ele1 = "R1 1 0 30K"

	node_dim, branch_dim = parse_element(ele1, node_dim, branch_dim)
	assert_equal(node_dim,2)
	assert_equal(branch_dim, 0)
	assert_equal(len(ELEMENT_LIST),1)
	assert_equal(ELEMENT_LIST[0].catagory,'r')
	assert_equal(ELEMENT_LIST[0].name,'r1')
	assert_equal(ELEMENT_LIST[0].value,3e04)
	assert_equal(ELEMENT_LIST[0].branch_flag,0)
	assert_equal(ELEMENT_LIST[0].active_flag,0)

	ele2 = "VIN 3 0 0.01 AC 1 35 SIN(0 1 1X)"
	node_dim, branch_dim = parse_element(ele2, node_dim, branch_dim)
	assert_equal(node_dim,3)
	assert_equal(branch_dim, 1)
	assert_equal(ELEMENT_LIST[1].branch, 0)
	assert_equal(ELEMENT_LIST[1].branch_flag, 1)
	assert_equal(ELEMENT_LIST[1].ac_mag, 1)
	assert_equal(ELEMENT_LIST[1].ac_phase, 35)
	assert_equal(ELEMENT_LIST[1].tran.freq, 1e06)

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











