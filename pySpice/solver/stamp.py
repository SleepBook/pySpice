import pySpice.global_data
from pySpice.element_class import *
import math
from itertools import tee
import pdb

def stamp(analysis_type, analysis_instance, MNA, RHS):
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
			if analysis_type == 'dc':				
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
			if analysis_type == 'dc':
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
			if analysis_type == 'dc':
				continue

			elif analysis_type == 'ac':
				sweep_flag = 1
				if element.catagory == 'c':
					imped = 1./((0+1j)*2*math.pi*element.value)
					coord = [((element.loc_p, element.loc_p),imped), ((element.loc_p, element.loc_n),0-imped), \
					((element.loc_n, element.loc_p),0-imped), ((element.loc_n, element.loc_n),imped)]
				
				elif element.catagory == 'l':
					imped = (0+1j)*2*math.pi*element.value
					coord = [((element.loc_p, element.loc_p), imped), ((element.loc_p, element.loc_n),0-imped), \
					((element.loc_n, element.loc_p),0-imped), ((element.loc_n, element.loc_n),imped)]

				temp = sweep_item('gen',coord)
				analysis_instance.generator, temp_gene = tee(analysis_instance.generator)
				temp.generator = temp_gene
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
				converge_flag = 1
				
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
	if src.catagory == 'sin':
		return sin_generator(src.freq, src.vdd, src.vgnd, tran_gene)
	elif src.catagory == 'pulse':
		return pulse_generator(src.td, src.tr, src.pw, src.tf, src.per, src.vdd, src.vgnd, tran_gene)


def sin_generator(freq, vdd, gnd, tran_gene):
	for time in tran_gene:
		yield math.sin(2*math.pi*freq*time)


def pulse_generator(td, tr, pw, tf, per, vdd, gnd, tran_gene):
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
				yield vdd - time * (vdd - gnd)/tf
			else:
				yield gnd


