import pySpice.global_data

def extract(unit_value):
	'''
	Extrace Spice Format Value
	
	The number used in Netlist often have a postfix unit, this function extrace this representation.

	:param unit_value: value represent in SPICE Netlist fashion
	:return: value in scientific representation
	'''
	if unit_value[-1] == 'k':
		value=float(unit_value[:-1])*1e03
	elif unit_value[-1] == 'x':
		value = float(unit_value[:-1])*1e06
	elif unit_value[-1] == 'g':
		value = float(unit_value[:-1])*1e09
	elif unit_value[-1] == 'm':
		value = float(unit_value[0:-1])*1e-03
	elif unit_value[-1] == 'u':
		value = float(unit_value[0:-1])*1e-06
	elif unit_value[-1] == 'n':
		value = float(unit_value[0:-1])*1e-09
	elif unit_value[-1] == 'p':
		value = float(unit_value[0:-1])*1e-12
	elif unit_value[-1] == 'f':
		value = float(unit_value[0:-1])*1e-15
	else:
		value = float(unit_value)
		
	return value

def address_transform(label, node_dim):
	'''
	Transform External Node Name into Internal Node Representation

	Basically, it check whether the label has already assigned an internal, if so, it will just return this internal representation. Otherwise, it will generate a new internal node number and plus the total node counter by 1
	
	:param label: External node name, a string
	:param node_dim: How many nodes the circuit current have
	:return:
		The previous node_dim and current node_dim
	'''
	if not (label in pySpice.global_data.NODE_TRANSLATION.keys()):
		pySpice.global_data.NODE_TRANSLATION[label] = node_dim
		node_dim += 1
		return node_dim-1, node_dim
	else:
		return pySpice.global_data.NODE_TRANSLATION[label], node_dim

def linear_generator(start, stop, step):
	"""
	Make a python generator based on the parameter. This generator will output data with linear interval
	"""
	
	temp = start
	if step > 0:
		while temp <= stop:
			yield temp
			temp += step
	else:
		while temp >= stop:
			yield temp
			temp += step

def dec_generator(start, stop, step):
	"""
	Make a python generator based on the parameter. This generator will output data with decimal interval
	"""
	temp = start
	factor = pow(10, 1./step)
	while temp <= stop:
		yield temp
		temp *= factor

def oct_generator(start, stop, step):
	"""
	Make a python generator based on the parameter. This generator will output data with octoal interval
	"""
	temp = start
	factor = pow(8, 1./step)
	while temp <= stop:
		yield temp
		temp *= factor
		
	
