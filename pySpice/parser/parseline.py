import pySpice.global_data
from pySpice.element_class import *
from pySpice.parser.utils import *
import re
import math
import pdb

def parse_element(raw_line, node_dim, branch_dim):
	'''docstring
	'''
	line = raw_line.strip().lower().split()

	if line[0][0] == 'r':
		value = 1./extract(line[3])
		ext_p = line[1]
		ext_n = line[2]
		loc_p, node_dim = address_transform(ext_p, node_dim)
		loc_n, node_dim = address_transform(ext_n, node_dim)
		name = line[0]
		catagory = 'r'
		temp = ele_2port(catagory,name,loc_p,loc_n,value)
		pySpice.global_data.ELEMENT_DICT[name] = temp

	elif line[0][0] == 'e':
		name = line[0]
		ext_p = line[1]
		ext_n = line[2]
		ext_ctrl_p = line[3]
		ext_ctrl_n = line[4]
		value = extract(line[5])
		loc_p, node_dim = address_transform(ext_p, node_dim)
		loc_n, node_dim = address_transform(ext_n, node_dim)
		loc_ctrl_p, node_dim = address_transform(ext_ctrl_p, node_dim)
		loc_ctrl_n, node_dim = address_transform(ext_ctrl_n, node_dim)
		brch_num, branch_dim = address_transform(name, branch_dim)
		temp = vcvs(loc_ctrl_p, loc_ctrl_n, brch_num, 'e', name, loc_p, loc_n, value)
		pySpice.global_data.ELEMENT_DICT[name] = temp

	elif line[0][0] == 'f':
		name = line[0]
		ext_p = line[1]
		ext_n = line[2]
		ext_ctrl_name = line[3]
		value = extract(line[4])
		loc_p, node_dim = address_transform(ext_p, node_dim)
		loc_n, node_dim = address_transform(ext_n, node_dim)
		loc_ctrl_brch, branch_dim = address_transform(ext_ctrl_name, branch_dim)
		temp = cccs(loc_ctrl_brch, 'f', name, loc_p, loc_n, value)
		pySpice.global_data.ELEMENT_DICT[name] = temp

	elif line[0][0] == 'g':
		name = line[0]
		ext_p = line[1]
		ext_n = line[2]
		ext_ctrl_p = line[3]
		ext_ctrl_n = line[4]
		value = extract(line[5])
		loc_p, node_dim = address_transform(ext_p, node_dim)
		loc_n, node_dim = address_transform(ext_n, node_dim)
		loc_ctrl_p, node_dim = address_transform(ext_ctrl_p, node_dim)
		loc_ctrl_n, node_dim = address_transform(ext_ctrl_n, node_dim)
		temp = vccs(loc_ctrl_p, loc_ctrl_n, 'g', name, loc_p, loc_n, value)
		pySpice.global_data.ELEMENT_DICT[name] = temp

	elif line[0][0] == 'h':
		name = line[0]
		loc_p, node_dim = address_transform(line[1], node_dim)
		loc_n, node_dim = address_transform(line[2], node_dim)
		loc_ctrl_brch, branch_dim = address_transform(line[3], branch_dim)
		value = extract(line[4])
		loc_brch, branch_dim = address_transform(name, branch_dim)
		temp = ccvs(loc_brch, loc_ctrl_brch, 'g', name, loc_p, loc_n, value)
		pySpice.global_data.ELEMENT_DICT[name] = temp
		
	elif line[0][0] == 'c' or line[0][0] == 'l':
		name = line[0]
		loc_p, node_dim = address_transform(line[1], node_dim)
		loc_n, node_dim = address_transform(line[2], node_dim)
		value = extract(line[3])
		if name[0] == 'c':
			temp = capacitor('c', name, loc_p, loc_n, value)
		else:
			loc_brch, branch_dim = address_transform(name, branch_dim) 
			temp = inductor(loc_brch, 'l', name, loc_p, loc_n, value)
			
		if (len(line) == 5 and line[4][1:3] == 'ic'):
			temp.ic = (line[4].split('='))[1][:-1]
			#current only support format like: IC=3v
		pySpice.global_data.ELEMENT_DICT[name] = temp

	elif line[0][0] == 'd':
		name = line[0]
		loc_p, node_dim = address_transform(line[1], node_dim)
		loc_n, node_dim = address_transform(line[2], node_dim)
		model = line[3]
		temp = diode(model, 'd', name, loc_p, loc_n, 0)
		m = re.search("ic=[0-9]*\?.[0-9]*[numkxg]?", raw_line.lower())
		if m != None:
			ic = extract(m.group().split('=')[1])
			temp.ic = ic
		pySpice.global_data.ELEMENT_DICT[name] = temp

	elif line[0][0] == 'm':
		#current only support w/l parmeter
		name = line[0]
		loc_d, node_dim = address_transform(line[1], node_dim)
		loc_g, node_dim = address_transform(line[2], node_dim)
		loc_s, node_dim = address_transform(line[3], node_dim)
		loc_b, node_dim = address_transform(line[4], node_dim)
		model = line[5]
		temp = mos(name, model, loc_d, loc_g, loc_s, loc_b)
		m = re.search("l=[0-9]*\.?[0-9]*[numkxg]?",raw_line.lower())
		if m != None:
			temp.l = extract(m.group().split('=')[1])
		m = re.search("w=[0-9]*\.?[0-9]*[numkxg]?",raw_line.lower())
		if m != None:
			temp.w = extract(m.group().split('=')[1])
		pySpice.global_data.ELEMENT_DICT[name] = temp

	elif (line[0][0] == 'v' or line[0][0] == 'i'):
		name = line[0]
		loc_p, node_dim = address_transform(line[1], node_dim)
		loc_n, node_dim = address_transform(line[2], node_dim)
		if name[0] == 'v':
			loc_brch, branch_dim = address_transform(name, branch_dim)
			temp = v_src(loc_brch, 'v', name, loc_p, loc_n, 0)
		else:
			temp = i_src('i', name, loc_p, loc_n, 0)
			
		if len(line) > 3:
			if line[3] == 'dc':
				temp.value = extract(line[4])
			else:
				m = re.match("-?[0-9]*\.?[0-9]*[numkxgNUMKXG]?",line[3])
				if m!= None:
					temp.value = extract(line[3])

			m = re.search("ac\s+[0-9]+[numkxg]?\s+[0-9]*", raw_line.lower())
			if m != None:
				buf = m.group().split()
				num = len(buf)
				ac_mag = extract(buf[1])
				ac_phase = 0
				if num == 3:
					ac_phase = eval(buf[2])
				real = ac_mag * math.cos(math.pi * ac_phase/180)
				imag = ac_mag * math.sin(math.pi * ac_phase/180)
				temp.ac = complex(real, imag)
			m = re.search("sin|exp|pulse",raw_line.lower())
			if m != None:
				buf = raw_line.lower()[m.span()[0]:] #assume this part must appear last
				tf = parse_timefunc(buf)
				temp.tran = tf
		pySpice.global_data.ELEMENT_DICT[name] = temp
				
	return node_dim, branch_dim

	
def parse_timefunc(string):
	if re.match('pulse',string) != None:
		string = string[5:]
		temp = string.find('(')
		if temp != -1:
			string = string[temp+1:]
			temp = string.find(')')
			string = string[:temp]
		buf = string.split()
		item = pulse_src(extract(buf[0]),extract(buf[1]), extract(buf[2][:-1]), extract(buf[3][:-1]), extract(buf[4][:-1]),extract(buf[5][:-1]), extract(buf[6][:-1]))
		return item

	elif re.match('sin',string) != None:
		string = string[3:]
		temp = string.find('(')
		if temp != -1:
			string = string[temp+1:]
			temp = string.find(')')
			string = string[:temp]
		buf = string.split()
		item = sin_src(extract(buf[0]), extract(buf[1]), extract(buf[2]))
		return item

	elif re.match('exp',string) != None:
		print "exp haven't support"
		return -1

	else:
		print "Unrecognied Time-Function Indep. Source"
		print "error raised, exiting now"
		return -1
			
			

def parse_ctrl(raw_line):
	"""Parse Dot Cmds
	#to do
	"""

	line = raw_line.strip().lower().split()
	if line[0][1:] == 'options':
		pass
		
	elif line[0][1:] == 'nodeset':
		pass

	elif line[0][1:] == 'ic':
		pass

	elif line[0][1:] == 'op':
		pySpice.global_data.ANALYSIS_LIST.append(1)
		
	elif line[0][1:] == 'dc':
		start_l = extract(line[2])
		stop_l = extract(line[3])
		step_l = extract(line[4])
		temp_gen = linear_generator(start_l, stop_l, step_l)		
		temp = analysis_dc(line[1], temp_gen)
		if len(line) > 5:
			temp.double_scan_flag = 1
			temp.generator2 = linear_generator(extract(line[6]), extract(line[7]), extract(line[8]))
			temp.swp_src2 = line[5]
		pySpice.global_data.ANALYSIS_LIST.append(temp)
			
	elif line[0][1:] == 'ac':
		if line[1] == 'lin':
			start_l = extract(line[3])
			stop_l = extract(line[4])
			step_l = (stop_l - start_l)/extract(line[2])
			temp_gen = linear_generator(start_l, stop_l, step_l)
		elif line[1] == 'oct':
			start_l = extract(line[3])
			stop_l = extract(line[4])
			step_l = extract(line[2])
			temp_gen = oct_generator(start_l, stop_l, step_l)
		elif line[1] == 'dec':
			start_l = extract(line[3])
			stop_l = extract(line[4])
			step_l = extract(line[2])
			temp_gen = dec_generator(start_l, stop_l, step_l)
		temp = analysis_ac(temp_gen)
		pySpice.global_data.ANALYSIS_LIST.append(temp)

	elif line[0][1:] == 'tran':
		start_l = 0
		stop_l = extract(line[2][:-1])
		step_l = extract(line[1][:-1])
		temp = analysis_tran(linear_generator(0, stop_l, step_l), step_l)
		if(re.search('uic', raw_line.lower()) != None):
			temp.uic_flag = 1;
		if len(line) > 3:
			if line[3] != 'uic':
				temp.show_start = extract(line[3][:-1])
				if len(line) > 4 and line[4] != 'uic':
					temp.max_step = extract(line[4][:-1])
		pySpice.global_data.ANALYSIS_LIST.append(temp)

	elif (line[0][1:] == 'print') or (line[0][1:] == 'plot'):
		for item in line[2:]:
			temp = print_item(item)
			if item[0] == 'v':
				if line[1] == 'ac':
					item = item[2:]
					temp.ac_flag = item[1]
				item = item.split('(')[1].split(')')[0]
				if item.find(',') != -1:
					temp.op_list.append(item.split(',')[0].strip())
					temp.op_list.append(item.split(',')[1].strip())
					temp.op_flag = 1
				else:
					temp.op_list.append(item[0].strip())

			elif item[0] == 'i':
				if line[1] == 'ac':
					item  = item[2:].strip('()')
					item.ac_flag = item[1]
				else:
					item = item[1:].strip('()')
				if item[0] != 'v':
					print "Current not support print device current except current source"
					print " Raise error"
					return -1
				else:
					temp.op_list.append(item.strip())
					temp.op_flag = 0

			if line[1] == 'dc':
				pySpice.global_data.PRINT_DICT['dc'].append(temp)
			elif line[1] == 'tran':
				pySpice.global_data.PRINT_DICT['tran'].append(temp)
			elif line[1] == 'ac':
				pySpice.global_data.PRINT_DICT['ac'].append(temp)
			else:
				print 'error'


		

			
					
					
						
		
		
	
				
				
		
	


