#This is the top module of the solver utility
from pySpice.element_class import *
from pySpice.solver.stamp import *
from pySpice.solver.engine import *
from itertools import tee
import pySpice.global_data
import numpy as np
import math

def solve():
	if 1 not in pySpice.global_data.ANALYSIS_LIST:
		print 'WARNING op not found in the netlist, doing OP automatically'
		single_solve('op')

	for instance in pySpice.global_data.ANALYSIS_LIST:
		if instance == 1:
			continue
		else:
			if instance.catagory == 'analy_ac':
				single_solve('ac',instance)
			elif instance.catagory == 'analy_dc':
				single_solve('dc', instance)
			elif instance.catagory == 'analy_tran':
				single_solve('tran', instance)
			else:
				print "unrecognized analysis, exiting"
				return -1


def single_solve(analysis_type, analysis_instance):
	#attention, here raise an critical question about python, that's whether the paramenter 
	#to a function is address-transfor or copy-transfor
	#actually the answer is either, and it depends on the data_type
	#in python, data has no type(actually it's all pointer to the heap), so, if the object the dataname 
	#point to is immutable, then pass it as an parameter will simply create new copy of this data, 
	#and this will behave like value-pass
	#if the data is muttable, however, then it will simpliy pass the link and this behave like address-pass

	#here, np.ndarray is mutable
	if analysis_type == 'ac':		
		MNA = np.zeros((pySpice.global_data.MNA_dim, pySpice.global_data.MNA_dim), dtype=np.complex)
		RHS = np.zeros((pySpice.global_data.MNA_dim,), dtype=np.complex)
		ANS = np.zeros((pySpice.global_data.MNA_dim,), dtype=np.complex)
	else:
		MNA = np.zeros((pySpice.global_data.MNA_dim, pySpice.global_data.MNA_dim), dtype=np.double)
		RHS = np.zeros((pySpice.global_data.MNA_dim,), dtype=np.double)
		ANS = np.zeros((pySpice.global_data.MNA_dim,), dtype=np.double)

	sweep_flag, sweep_list, converge_flag, converge_list = stamp(analysis_type, analysis_instance, MNA, RHS)

	if analysis_type == 'ac':
		raw_output = solve_engine(analysis_instance.iter_time, sweep_flag, sweep_list, converge_flag, converge_list, pySpice.global_data.watch_list['ac'], MNA, RHS, ANS)
	elif analysis_type == 'dc':
		raw_output = solve_engine(analysis_instance.iter_time, sweep_flag, sweep_list, converge_flag, converge_list, pySpice.global_data.watch_list['dc'], MNA, RHS, ANS)
	elif analysis_type == 'tran':
		raw_output = solve_engine(analysis_instance.iter_time, sweep_flag, sweep_list, converge_flag, converge_list, pySpice.global_data.watch_list['tran'], MNA, RHS, ANS)

	scan_bar = []
	for cursor in analysis_instance.generator:
		scan_bar.append(cursor)
	raw_output.append(scan_bar)
	
	return raw_output