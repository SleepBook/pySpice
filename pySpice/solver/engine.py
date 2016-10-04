import pySpice.global_data
import numpy as np
from math import exp
import pdb

def solve_engine(sweep_flag, sweep_list, converge_flag, converge_list, watch_list, MNA, RHS, ANS):
	"""
	Top-Level Encapsulation of the Matrix Solving Utility

	This layer realizes the *iterate* operation support. This function controls to elicit the core matrix-solving utility at each step of the iteraion and at the same time change the stamping of MNA and RHS to represent different initial status of the circuit. 

	An graphical illustration of this module can be found below

	.. figure:: ../figures/engine.png

	:param sweep_flag: described at function stamp
	:param converge_flag: described at function stamp
	:param sweep_list: described at function stamp
	:param converge_list: described at function stamp
	:param watch_list: a list describe which node/branch's value are of interest. When everytime the solution of the circuit is reached, only the data for these points will be kept.
	:param MNA: stamped MNA
	:param RHS: stamped RHS
	:param ANS: The solution to the matrix equation. The reason for introduce it as a parameter is only for simplify the iteration process. Because for some element, the value to stamp for next iteration do not come from the generaor, but the answer of the previous iteration(like dynamic elements in transient analysis), so introducing such a parameter and set it's initial value to 0 and avoid unnecessary branches.
	:return: The value of all sweep points to the nodes/branches appeared on the watch_list
	"""
	if watch_list != 0:
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
		return  state_log

	else:
		ANS = state_definer(converge_flag, converge_list, MNA, RHS)
		return ANS


def state_definer(converge_flag, converge_list, MNA, RHS):
	"""
	Work out the Answer to the matrix equation, make sure the answer converge to the real state

	An inner layer of the engine utility, it encapsualte the functionality to solve circuit state by working out the matrix equation. The mechanism to ensure the answer converge is included into this function. 
	: param : Stated in *solve_engine* function
	: return: the raw answer of the matrix equation. Thses values are picked out at the outter layer
	"""
	if converge_flag:
		converge_indicator = []
		state_previous = []
		for element in converge_list:
			converge_indicator.append(0)
			if element.catagory == 'd':
				#state_previous.append([0,0,40,0]) this is actually wrong, the circuit will never start
				state_previous.append([0,0,0,0])
				#rerpesent voltage cross, current, previous_admitance, previous_bias respectively
			elif element.catagory == 'mos':
				state_previous.append([1,0,0,0,0])
				#represent Vgs Vds Gds Ggs bias

		while (0 in converge_indicator):
			print 'iteronce'
			for i in range(len(converge_indicator)):
				converge_indicator[i] = 0			
			
			for i,element in enumerate(converge_list):
				if element.catagory == 'd':
					if element.model == 'diode':
						#i think lamda function should fit in here
						#admitance =
						admitance = (40*exp(40*state_previous[i][0]))
						bias = state_previous[i][1] - admitance*state_previous[i][0]
					else:
						#other model
						print 'not support other diode model currently'
					
					MNA[element.loc_p, element.loc_p] += admitance
					MNA[element.loc_p, element.loc_n] += 0 - admitance
					MNA[element.loc_n, element.loc_p] += 0 - admitance 
					MNA[element.loc_n, element.loc_n] += admitance
					RHS[element.loc_p] += 0 - bias
					RHS[element.loc_n] += bias
					state_previous[i][2] = admitance
					state_previous[i][3] = bias

				elif element.catagory == 'mos':					
					vgs = state_previous[i][0]
					vds = state_previous[i][1]
					if element.model == 'nmos' and vds < 0 :
						vds = 0
					elif element.model == 'pmos' and vds > 0:
						vds = 0
					if element.model == 'nmos':
						vth = pySpice.global_data.VTH_NMOS
						k = pySpice.global_data.K_NMOS
						lamda = pySpice.global_data.LAMDA_NMOS
						if vgs < vth:
							region = 0
						elif vds < (vgs - vth):
							region = 1
						elif vds > (vgs - vth):
							region = 2
					elif element.model == 'pmos':
						vth = pySpice.global_data.VTH_PMOS
						k = pySpice.global_data.K_PMOS
						lamda = pySpice.global_data.LAMDA_PMOS
						if vgs - vth > 0:
							region = 0
						elif vds < vgs - vth:
							region = 2
						elif vds > vgs - vth:
							region = 1

					if region == 0:
						Ggs = 0.0
						Gds = 0.0
						Id = 0.0
						bias = 0.0
					elif region == 1:
						Ggs = k* element.w * vds*(1+ lamda*vds)/element.l
						Gds = k*element.w*(2*(vgs-vth)*(1+2*lamda*vds)-2*vds-3*lamda*pow(vds,2))/(2*element.l)
						if vds>0:
							Id = k*element.w*(2*(vgs-vth)*vds - pow(vds,2))*(1+lamda*vds)/(element.l * 2)
						else:
							Id = k*element.w*(2*(vgs-vth)*vds - pow(vds,2))/(element.l * 2)
						bias = Id - (Ggs*vgs + Gds*vds)

					elif region == 2:
						Ggs = k * element.w *(1+lamda*vds)*(vgs - vth)/element.l
						Gds = k * element.w * pow((vgs - vth),2) * lamda/(2*element.l)
						Id = k*element.w*pow((vgs-vth),2)*(1+lamda*vds)/(2*element.l)
						bias = Id - (Ggs*vgs + Gds*vds)					

					MNA[element.loc_d, element.loc_d] += Gds
					MNA[element.loc_d, element.loc_s] += 0-Gds-Ggs
					MNA[element.loc_d, element.loc_g] += Ggs
					MNA[element.loc_s, element.loc_d] += 0-Gds
					MNA[element.loc_s, element.loc_s] += Gds + Ggs
					MNA[element.loc_s, element.loc_g] += 0-Ggs
					RHS[element.loc_d] += 0-bias
					RHS[element.loc_s] += bias

					state_previous[i][2] = Gds
					state_previous[i][3] = Ggs
					state_previous[i][4] = bias

			local_ans = np.linalg.solve(MNA[1:,1:], RHS[1:])
			local_ans = np.insert(local_ans, 0, 0.0)

			for i, element in enumerate(converge_list):
				if element.catagory == 'd':
					admitance = state_previous[i][2]
					bias = state_previous[i][3]

					MNA[element.loc_p, element.loc_p] -= admitance 
					MNA[element.loc_p, element.loc_n] -= 0 - admitance 
					MNA[element.loc_n, element.loc_p] -= 0 - admitance
					MNA[element.loc_n, element.loc_n] -= admitance
					RHS[element.loc_p] -= 0 - bias
					RHS[element.loc_n] -= bias

					cross_voltage = local_ans[element.loc_p] - local_ans[element.loc_n]
					if element.model == 'diode':
						current = exp(40*cross_voltage) - 1
					else:
						print 'not support other diode model currently'

					if abs((cross_voltage - state_previous[i][0])) <= pySpice.global_data.CONVERGE_CRITERIA and abs((current - state_previous[i][1])) <= pySpice.global_data.CONVERGE_CRITERIA:
						converge_indicator[i] = 1
			
					state_previous[i][0] = cross_voltage
					state_previous[i][1] = current

				elif element.catagory == 'mos':
					Gds = state_previous[i][2]
					Ggs = state_previous[i][3]
					bias = state_previous[i][4]
					vgs = state_previous[i][0]
					vds = state_previous[i][1]

					MNA[element.loc_d, element.loc_d] -= Gds
					MNA[element.loc_d, element.loc_s] -= 0-Gds-Ggs
					MNA[element.loc_d, element.loc_g] -= Ggs
					MNA[element.loc_s, element.loc_d] -= 0-Gds
					MNA[element.loc_s, element.loc_s] -= Gds + Ggs
					MNA[element.loc_s, element.loc_g] -= 0-Ggs
					RHS[element.loc_d] -= 0-bias
					RHS[element.loc_s] -= bias
					
					vgs_new = local_ans[element.loc_g] - local_ans[element.loc_s]
					vds_new = local_ans[element.loc_d] - local_ans[element.loc_s]

					if abs(vgs_new - vgs) <= pySpice.global_data.CONVERGE_CRITERIA and abs(vds_new - vds) <= pySpice.global_data.CONVERGE_CRITERIA:
						converge_indicator[i] = 1

					#pdb.set_trace()
					state_previous[i][0] = vgs_new
					state_previous[i][1] = vds_new

		#pdb.set_trace()
		return local_ans

	else:
		#pdb.set_trace()
		local_ans = np.linalg.solve(MNA[1:,1:], RHS[1:])
		return np.insert(local_ans,0,0.0)
