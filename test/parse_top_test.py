from nose.tools import *
from pySpice.parser.parseline import *
from pySpice.parser.parser import *
import pySpice.global_data 
from pySpice.parser.utils import *
import pdb

def test_parse_top():
	reload(pySpice.global_data)
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'resistor.sp')
	assert_equal(pySpice.global_data.MNA_dim, 4)
	

if __name__ == '__main__':
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'double_diode.sp')
	pdb.set_trace()
	
