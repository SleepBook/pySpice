import pySpice.global_data
import numpy as np

"""
This is the key module inside the solver utility
"""

def solve_engine(iter_time, sweep_flag, sweep_list, converge_flag, converge_list, watch_list, MNA, RHS, ANS):
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

	for i in range(iter_time):
		for sweep_item in sweep_list:
			if sweep_item.switch == 'gen':
				value = sweep_item.generator.next()
			elif sweep_item.switch == 'upd':
				value = 0
				for j in range(len(update_src)):
					value = value + ANS[update_src[j][0][0]]*update_src[j][1]
			
			for j in range(len(sweep_item.coord)):
				if len(sweep_item.coord[j][0])==1:
					RHS[sweep_item.coord[j][0][0]] = value*sweep_item.coord[j][1]
				elif len(sweep_item.coord[j][0])==2:
					MNA[sweep_item.coord[j][0][0], sweep_item.coord[j][0][1]] = value*sweep_item.coord[j][1]

		state_definer(converge_flag, converge_list, MNA, RHS, ANS)

		for j, script in enumerate(watch_list):
			state_log[j].append(ANS[watch_list[script]])

	return state_log



def state_definer(converge_flag, converge_list, MNA, RHS, ANS):
	"""
	Solve the Matrix, including handling the convergence issue"""
	if converge_flag:
		pass
		print 'not diode yet'

	else:
		ANS = np.linalg.solve(MNA, RHS)


