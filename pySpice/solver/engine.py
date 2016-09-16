import pySpice.global_data
import numpy as np
from math import exp
import pdb

"""
This is the key module inside the solver utility
"""

def solve_engine(sweep_flag, sweep_list, converge_flag, converge_list, watch_list, MNA, RHS, ANS):
	"""
	Abstract the Circuit Resolver's Mathmatic and Systematic Behavior

	To say, solve the circuit equals solving the MNA-RHS matrix equation. And do
	a thourough analysis may wrap this solving in several layers.
	First, solve a single point may involve iteration, this happens when non-linear
	elements(diode, mosfet) get involves. Second, do the scan-like analysis(DC sweep,
	ac and tran) need to do a sequence of matrix solving, with each time change the MNA
	or RHS a bit.
	So generally we can abstract general analysis as follows, the outsider(we name it, sweeper) need to
	take care of the sweep staff(change the parameters and do repetitive matrix solving), 
	within each solving, the inner layer take care of the converge issue.
	along the way, the engine also read in the watchlist and generate the output raw data
	"""
	state_log = []
	for i in range(len(watch_list)):
		state_log.append([])
	if sweep_flag:
		value_previous = []
		for i in range(len(sweep_list)):
			value_previous.append(0)
		END_OF_SWEEP = 0
		while 1:	
			for i, sweep_item in enumerate(sweep_list):
				if sweep_item.switch == 'gen':
					if sweep_item.update_src == 0:
						try:
							value = sweep_item.generator.next()
						except StopIteration:
							END_OF_SWEEP = 1
							break
					else:
						#it's an ad-hoc remedy, in case the admitance of inductor is 1/f
						try:
							value = 1./sweep_item.generator.next()
						except StopIteration:
							END_OF_SWEEP = 1
							break
				elif sweep_item.switch == 'upd':
					value = 0
					for j in range(len(sweep_item.update_src)):
						value = value + ANS[sweep_item.update_src[j][0][0]]*sweep_item.update_src[j][1]
				
				for j in range(len(sweep_item.coord)):
					if len(sweep_item.coord[j][0]) == 1:
						RHS[sweep_item.coord[j][0][0]] += (value - value_previous[i])*sweep_item.coord[j][1]
					elif len(sweep_item.coord[j][0]) == 2:
						MNA[sweep_item.coord[j][0][0], sweep_item.coord[j][0][1]] += (value - value_previous[i])*sweep_item.coord[j][1]
				value_previous[i] = value

			if END_OF_SWEEP:
				break
			ANS = state_definer(converge_flag, converge_list, MNA, RHS)
			for j, script in enumerate(watch_list):
				state_log[j].append(ANS[script])
			

	return state_log



def state_definer(converge_flag, converge_list, MNA, RHS):
	"""
	Solve the Matrix, including handling the convergence issue"""
	if converge_flag:
		converge_indicator = []
		state_previous = []
		for element in converge_list:
			converge_indicator.append(0)
			if element.catagory == 'd':
				#state_previous.append([0,0,40,0]) this is actually wrong, the circuit will never start
				state_previous.append([0,0,0,0])
				#rerpesent voltage cross, current, previous_admitance, previous_bias respectively
			elif element.catagory == 'm':
				pass

		while (0 in converge_indicator):
			for i,element in enumerate(converge_list):
				if element.catagory == 'd':
					if element.model == 'diode':
						#i think lamda function should fit in here
						#admitance =
						admitance =  40*exp(40*state_previous[i][0])
						bias = state_previous[i][1] - admitance*state_previous[i][0]
					else:
						#other model
						print 'not support other diode model currently'
					previous_admitance = state_previous[i][2]
					previous_bias = state_previous[i][3]						

					MNA[element.loc_p, element.loc_p] += admitance - previous_admitance
					MNA[element.loc_p, element.loc_n] += 0 - admitance + previous_admitance
					MNA[element.loc_n, element.loc_p] += 0 - admitance + previous_admitance
					MNA[element.loc_n, element.loc_n] += admitance - previous_admitance
					RHS[element.loc_p] += 0 - bias + previous_bias
					RHS[element.loc_n] += bias - previous_bias
					state_previous[i][2] = admitance
					state_previous[i][3] = bias

				elif element.catagory == 'm':
					pass
					
			local_ans = np.linalg.solve(MNA[1:,1:], RHS[1:])
			local_ans = np.insert(local_ans, 0, 0.0)

			for i, element in enumerate(converge_list):
				if element.catagory == 'd':
					cross_voltage = local_ans[element.loc_p] - local_ans[element.loc_n]
					if element.model == 'diode':
						current = exp(40*cross_voltage) - 1
					else:
						print 'not support other diode model currently'
					if abs(cross_voltage - state_previous[i][0]) <= pySpice.global_data.CONVERGE_CRITERIA:
						converge_indicator[i] = 1
			
					state_previous[i][0] = cross_voltage
					state_previous[i][1] = current

				elif element.catagory == 'm':
					pass
					#haven't support mosfet yet
		return local_ans

	else:
		#pdb.set_trace()
		local_ans = np.linalg.solve(MNA[1:,1:], RHS[1:])
		return np.insert(local_ans,0,0.0)