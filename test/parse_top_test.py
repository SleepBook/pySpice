#from nose.tools import *
from pySpice.parser.parseline import *
from pySpice.parser.parser import *
import pySpice.global_data 
from pySpice.parser.utils import *
import pdb

def test_parse_top():
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'resistor.sp')
	

if __name__ == '__main__':
	NETLIST_ROOT = 'data/sample_netlist/'
	parser(NETLIST_ROOT + 'resistor.sp')
	pdb.set_trace()
	
