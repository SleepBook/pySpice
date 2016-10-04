from pySpice.element_class import *
from pySpice.solver.stamp import *
from pySpice.solver.engine import *
from itertools import tee
import pySpice.global_data
import numpy as np
import math
import pdb

def solve():
	"""
	Top Level Encapsuation of the Utilities to Determine the Circuit's State

	:Return:
		output(watchpoint_data) is a 3-D array, if assume the three coordinate of this array to be output[z][x][y]. Then each slices of z direction represent the output of either DC/AC/TRAN analysis. Within each Z frame, the X represent the watchlist item which is parsed in parsing phase and the x values is the values solved in each iteration. 
	"""
	
	watchpoint_data = {}
	if 1 not in pySpice.global_data.ANALYSIS_LIST:
		print 'WARNING op not found in the netlist, doing OP automatically'
	initial_state = single_solve(0)
	pySpice.global_data.INIT_STATE = np.copy(initial_state)

	for instance in pySpice.global_data.ANALYSIS_LIST:
		if instance == 1:
			continue
		else:
			output = single_solve(instance)
			watchpoint_data[instance.catagory] = output
	return watchpoint_data



def single_solve(analysis_instance):
	"""
	Sub-Utility of Solve Function, Perform the Perform on a Single Analysis Type
	
	:param analysis_instance: internal data structure representing the analysis commands
	:return:
		A single frame of the output structure illustracted in figure x.x

	"""
	#attention, here raise an critical question about python, that's whether the paramenter 
	#to a function is address-transfor or copy-transfor
	#actually the answer is either, and it depends on the data_type
	#in python, data has no type(actually it's all pointer to the heap), so, if the object the dataname 
	#point to is immutable, then pass it as an parameter will simply create new copy of this data, 
	#and this will behave like value-pass
	#if the data is muttable, however, then it will simpliy pass the link and this behave like address-pass

	#here, np.ndarray is mutable
	if analysis_instance == 0:
		analysis_type = 'op'
	else:
		analysis_type = analysis_instance.catagory
	
	if analysis_type == 'ac':		
		MNA = np.zeros((pySpice.global_data.MNA_dim, pySpice.global_data.MNA_dim), dtype=np.complex)
		RHS = np.zeros((pySpice.global_data.MNA_dim,), dtype=np.complex)
		ANS = np.zeros((pySpice.global_data.MNA_dim,), dtype=np.complex)
	else:
		MNA = np.zeros((pySpice.global_data.MNA_dim, pySpice.global_data.MNA_dim), dtype=np.double)
		RHS = np.zeros((pySpice.global_data.MNA_dim,), dtype=np.double)
		ANS = np.zeros((pySpice.global_data.MNA_dim,), dtype=np.double)

	sweep_flag, sweep_list, converge_flag, converge_list = stamp(analysis_type, analysis_instance, MNA, RHS)
	if analysis_type == 'op':
		raw_output = solve_engine(0, [], converge_flag, converge_list, 0, MNA, RHS, ANS)
	elif analysis_type == 'ac':
		raw_output = solve_engine(sweep_flag, sweep_list, converge_flag, converge_list, pySpice.global_data.watch_list['ac'], MNA, RHS, ANS)
	elif analysis_type == 'dc':
		raw_output = solve_engine(sweep_flag, sweep_list, converge_flag, converge_list, pySpice.global_data.watch_list['dc'], MNA, RHS, ANS)
	elif analysis_type == 'tran':
		raw_output = solve_engine(sweep_flag, sweep_list, converge_flag, converge_list, pySpice.global_data.watch_list['tran'], MNA, RHS, ANS)

	if analysis_type != 'op':
		scan_bar = []
		for cursor in analysis_instance.generator:
			scan_bar.append(cursor)
		#a bit messy, for raw_output is ndarray while scan_bar is list
		#overlook for now
		raw_output.append(scan_bar)
		
	return raw_output
	
