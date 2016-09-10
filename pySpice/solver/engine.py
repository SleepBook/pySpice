"""
This is the key module inside the solver utility
"""

def solve_engine(sweep_flag, sweep_list, converge_flag, converge_list, watch_list):
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
	
	#TO DO 
	pass
