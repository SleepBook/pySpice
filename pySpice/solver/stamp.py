import pySpice.global_data
from pySpice.element_class import *
import math
from itertools import tee
import pdb

def stamp(analysis_type, analysis_instance, MNA, RHS):
	"""
	Generating MNA and RHS to Represent the Circuit

	This function retrieve information from the internal structure to constitute MNA and RHS. It also collects neessary information for doing iterate and converge operations.

	:param analysis_type: 'ac', 'dc' or 'tran'
	:param analysis_instance: internal representation of an analysis command
	:param MNA: an initialized matrix, with date type defined
	:param RHS: an initialized vector, data type defined
	:return:
		+ **sweep_flag**: a bool flag, indicating if iterate meahanism needed to be actived in the engine.
		+ **converge_flag**: a bool flag, indicating if converge iteration should be actived
		+ **sweep_list**: a list of sweep_item. Each sweep_item contains the information indicating how the solve_engine should change the MNA and RHS in each step of the iteration.
		+ **converge_list**: a list of the element whose beahvior is non-linear.

	About the class *sweep_item*, it is comprised of two part: The second part is a generator. In each iteration, by calling the *.next()* method to this generator, it will give the value needed to be stamped in this iteration. The first part is a list of tuples, with each tuple's first element of a coordinate, indicating where to change the stamp. The second element to this tuple is a prefix, you need to multiply the value with this prefix to get the final value to be stamped in this position. Using generator is for memory reducing consideration.

	"""
	sweep_flag = 0
	converge_flag = 0
	sweep_list = []
	converge_list = []

	for element in pySpice.global_data.ELEMENT_DICT.values():
		if element.catagory == 'r':
			MNA[element.loc_p, element.loc_p] += element.value
			MNA[element.loc_p, element.loc_n] += 0 - element.value
			MNA[element.loc_n, element.loc_p] += 0 - element.value
			MNA[element.loc_n, element.loc_n] += element.value

		elif element.catagory == 'e':
			MNA[element.loc_p, element.branch] += 1
			MNA[element.loc_n, element.branch] += 0 - 1
			MNA[element.branch, element.loc_p] += 1
			MNA[element.branch, element.loc_n] += 0 - 1
			MNA[element.branch, element.loc_ctrl_p] += 0 - element.value
			MNA[element.branch, element.loc_ctrl_n] += element.value

		elif element.catagory == 'f':
			MNA[element.loc_p, element.loc_ctrl_branch] += element.value
			MNA[element.loc_n, element.loc_ctrl_branch] += 0 - element.value

		elif element.catagory == 'g':
			MNA[element.loc_p, element.loc_ctrl_p] += element.value
			MNA[element.loc_p, element.loc_ctrl_n] += 0 - element.value
			MNA[element.loc_n, element.loc_ctrl_p] += 0 - element.value
			MNA[element.loc_n, element.loc_ctrl_n] += element.value

		elif element.catagory == 'h':
			MNA[element.loc_p, element.branch] += 1
			MNA[element.loc_n, element.branch] += 0 - 1
			MNA[element.branch, element.loc_p] += 1
			MNA[element.branch, element.loc_p] += 0 - 1
			MNA[element.branch, element.loc_ctrl_branch] += 0 - element.value

		#stamping process varies with analysis type
		elif element.catagory == 'v':
			MNA[element.loc_p, element.branch] += 1
			MNA[element.loc_n, element.branch] += 0 - 1
			MNA[element.branch, element.loc_p] += 1
			MNA[element.branch, element.loc_n] += 0 - 1
			if analysis_type == 'op' or (analysis_type == 'dc' and analysis_instance.swp_src != element.name):				
				RHS[element.branch] += element.value
			elif analysis_type == 'ac':
				RHS[element.branch] += element.ac
			elif analysis_type == 'tran':
				sweep_flag = 1
				coord = [((element.branch,),1)]
				temp = sweep_item('gen',coord)
				analysis_instance.generator, temp_gene = tee(analysis_instance.generator)
				temp.generator = make_generator(element.tran, temp_gene)		
				sweep_list.append(temp)				

		elif element.catagory == 'i':
			if analysis_type == 'op' or (analysis_type == 'tran' and analysis_instance.swp_src != element.name):
				RHS[element.loc_p] += 0 - element.value
				RHS[element.loc_n] += element.value
			elif analysis_type == 'ac':
				RHS[element.loc_p] += 0 - element.ac
				RHS[element.loc_n] += element.ac
			elif analysis_type == 'tran':
				sweep_flag = 1
				coord = [((element.loc_n,),1),((element.loc_p,),-1)]
				temp = sweep_item('gen',coord)
				analysis_instance.generator, temp_gene = tee(analysis_instance.generator)
				temp.generator = make_generator(element.tran, temp_gene)
				sweep_list.append(temp)

		elif element.catagory == 'c' or element.catagory == 'l':
			if analysis_type == 'dc' or analysis_type == 'op':
				if element.catagory == 'l':
					MNA[element.loc_p, element.branch] += 1
					MNA[element.loc_n, element.branch] += 0-1
					MNA[element.branch, element.loc_p] += 1
					MNA[element.branch, element.loc_n] += 0-1
					
			elif analysis_type == 'ac':
				sweep_flag = 1
				if element.catagory == 'c':
					admitance = ((0+1j)*2*math.pi*element.value)
					coord = [((element.loc_p, element.loc_p),admitance), ((element.loc_p, element.loc_n),0-admitance), \
					((element.loc_n, element.loc_p),0-admitance), ((element.loc_n, element.loc_n),admitance)]
				
				elif element.catagory == 'l':
					admitance = 1./((0+1j)*2*math.pi*element.value)
					#coord = [((element.loc_p, element.loc_p), admitance), ((element.loc_p, element.loc_n),0-admitance), \
					#((element.loc_n, element.loc_p),0-admitance), ((element.loc_n, element.loc_n),admitance)]
					MNA[element.loc_p, element.branch] = 1
					MNA[element.loc_n, element.branch] = 0-1
					MNA[element.branch, element.branch] = 1
					coord = [((element.branch, element.loc_p), 0-admitance), ((element.branch, element.loc_n), admitance)]
				temp = sweep_item('gen',coord)
				analysis_instance.generator, temp_gene = tee(analysis_instance.generator)
				temp.generator = temp_gene
				temp.update_src = 1
				sweep_list.append(temp)


			elif analysis_type == 'tran':
				sweep_flag = 1
				if element.catagory == 'c':
					value = element.value/analysis_instance.step
					MNA[element.loc_p, element.loc_p] += value
					MNA[element.loc_p, element.loc_n] += 0 - value
					MNA[element.loc_n, element.loc_p] += 0 - value
					MNA[element.loc_n, element.loc_n] += value
					coord = [((element.loc_p,), value), ((element.loc_n,),0-value)]
					update_src = [((element.loc_p,), 1), ((element.loc_n,), 0-1)]
				elif element.catagory == 'l':
					value = element.value/analysis_instance.step
					MNA[element.loc_p, element.branch] += 1
					MNA[element.loc_n, element.branch] += 0-1
					MNA[element.branch, element.loc_p] += 1
					MNA[element.branch, element.loc_n] += 0-1
					MNA[element.branch, element.branch] += 0-value
					coord = [((element.branch,),0-value)]
					update_src = [((element.branch,),1)]

				temp = sweep_item('upd', coord)	
				temp.update_src = update_src
				sweep_list.append(temp)
			
		elif element.catagory == 'd':
			if analysis_type == 'ac':
				pass
			else:
				converge_flag += 1
				converge_list.append(element)
				#the actual stamping work for diode in transfered into the engine:state_definer
		elif element.catagory == 'mos':
			if analysis_type == 'ac':
				pass
			else:
				converge_flag += 1
				converge_list.append(element)

				
	if analysis_type == 'dc':
		sweep_flag = 1
		swp_src = pySpice.global_data.ELEMENT_DICT[analysis_instance.swp_src]
		if swp_src.catagory == 'v':
			coord = [((swp_src.branch,),1)]
		elif swp_src.catagory == 'i':
			coord = [((swp_src.loc_p,), -1), ((swp_src.loc_n,), 1)]
		temp = sweep_item('gen',coord)
		analysis_instance.generator, temp_gene = tee(analysis_instance.generator)
		temp.generator = temp_gene
		sweep_list.append(temp)

	return sweep_flag, sweep_list, converge_flag, converge_list


def make_generator(src, tran_gene):
	"""
	Make Generator out of the  Transinent Stimulates

	Because the stimulates for transinent analysis is defines with the voltage/current source, while the time step to transinent analysis is defined in the Transinent analysis command. It is not possible to make the generator describing the voltage/current at certain time point at parsing time. And this task in done here.

	This function is the and encapsulation, according to the type of the time varient stimulates, the actually work is assigned to different sub-routines
	"""
	if src.catagory == 'sin':
		return sin_generator(src.freq, src.vdd, src.vgnd, tran_gene)
	elif src.catagory == 'pulse':
		return pulse_generator(src.td, src.tr, src.pw, src.tf, src.per, src.vdd, src.vgnd, tran_gene)
	elif src.catagory == 'stair':
		return stair_generator(src.vdd, src.vgnd, src.up_moment, tran_gene)

def sin_generator(freq, vdd, gnd, tran_gene):
	"""
	Make generator describe sinusoidal variation
	"""
	
	for time in tran_gene:
		amp = (vdd - gnd)/2.0
		bias = (vdd + gnd)/2.0
		yield amp*math.sin(2*math.pi*freq*time) + bias

def stair_generator(vdd, gnd, up_moment, tran_gene):
	""" 
	Make genrator describing a step function
	"""

	for time in tran_gene:
		if time < up_moment:
			yield gnd
		else:
			yield vdd	

def pulse_generator(td, tr, pw, tf, per, vdd, gnd, tran_gene):
	"""
	Make generator describing pulse, with rise and falls
	"""

	for time in tran_gene:
		if time < td:
			yield gnd
		else:
			time = (time-td) % per
			if time < tr:
				yield time * (vdd - gnd)/tr + gnd
			elif time >= tr and time <(tr+pw):
				yield vdd
			elif time >= (tr+pw) and time <(tr+pw+tf):
				yield vdd + (time - tr - pw) * (gnd - vdd)/tf
			else:
				yield gnd


