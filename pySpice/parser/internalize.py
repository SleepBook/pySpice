import pySpice.global_data

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

	for item in pySpice.global_data.ELEMENT_DICT.values():
		if item.branch_flag == 1:
			item.branch = item.branch + node_dim
			pySpice.global_data.NODE_TRANSLATION[item.name] = item.branch
			if item.catagory == 'h':
				item.loc_ctrl_branch = item.loc_ctrl_branch + node_dim		

	for item in pySpice.global_data.PRINT_DICT['dc']:
		for num, point in enumerate(item.op_list):
			check_point = pySpice.global_data.NODE_TRANSLATION[point]
			item.op_list[num] = check_point
			if check_point not in pySpice.global_data.watch_list['dc']:
				pySpice.global_data.watch_list['dc'].append(check_point)

	for item in pySpice.global_data.PRINT_DICT['tran']:
		for num, point in enumerate(item.op_list):
			check_point = pySpice.global_data.NODE_TRANSLATION[point]
			item.op_list[num] = check_point
			if check_point not in pySpice.global_data.watch_list['tran']:
				pySpice.global_data.watch_list['tran'].append(check_point)

	for item in pySpice.global_data.PRINT_DICT['ac']:
		#TO DO
		pass

	