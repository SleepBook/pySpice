from pySpice.global_data import *

def internalize(node_dim):
	"""Convert External Node Name to Internal Node Name

	Part of the data after the parser part still use external 
	node name, this function is used to convert them. 
	At the same time, this module also unify the name sequence 
	of both node_dim and branch_dim(because when parsing the branch
	name also start from 0.
	After Conversion, the internal is essentially the row/colomn number
	of the MNA matrix(row 0/column 0 included)
	"""

	for item in ELEMENT_LIST.values():
		if item.branch_flag == 1:
			item.branch = item.branch + node_dim
			if item.catagory == 'h':
				item.loc_ctrl_branch = item.loc_ctrl_branch + node_dim

	for item in PRINT_DICT['dc']:
		for num, point in enumerate(item.op_list):
			check_point = NODE_TRANSLATION[point]
			item.op_list[num] = check_point
			if check_point not in watch_list['dc']:
				watch_list['dc'].append(check_point)

	for item in PRINT_DICT['tran']:
		for num, point in enumerate(item.op_list):
			check_point = NODE_TRANSLATION[point]
			item.op_list[num] = check_point
			if check_point not in watch_list['tran']:
				watch_list['tran'].append(check_point)

	for item in PRINT_DICT['ac']:
		#TO DO
		pass

	#TO_DO TRANSLATION_DICT