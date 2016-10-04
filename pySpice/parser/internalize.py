import pySpice.global_data

def internalize(node_dim):
	"""Convert External Node Name to Internal Node Number

    While parsing element, the practice of counting the total node number actually has an implicit function to convert the node name used by Netlist into internal representations of continuious integers, which will make it much easier to generate the matrix representing the circuit in *solver* phase. Essentially, thses integers are the row and coloum number representging that node in the matrix. 

    However, in parsing, we count node and branch(links between nodes) seperately, but in matrix they are processed as a whole. So this function modifies these number to give them a uniform sequence. 

    By the way, since we already got the information about the PRINT/PLOT commands, at this stage we also take notes of which nodes/branch's states are required in generating the final output report. Then we only log the states of these points in the *solver* phase to reduce intermediate data.

    :param node_dim: the total node number of the circuit

    :return:  
        Will modify the branch number to form an uniform sequence with node_dim. This will modify the ELEMENT_DICT and add content for the watch_list in global data
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
		for num, point in enumerate(item.op_list):
			check_point = pySpice.global_data.NODE_TRANSLATION[point]
			item.op_list[num] = check_point
			if check_point not in pySpice.global_data.watch_list['ac']:
				pySpice.global_data.watch_list['ac'].append(check_point)

	
