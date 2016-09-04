import pySpice.global_data

def extract(unit_value):
	'''
	this func convert a num with unit in string form to the value form
	unit_value: digit in char and a unit(n,u,m,k,x,g)
	output: the value
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
	this func is used to transform the list's node to loacl node, and decide how many branch needed
	namely this is to tranform the list's node to local matrix's coloum/row number
	at present, it still get to params from the parse stage, but these are not necessary

	at present it's only a qsudo realzation, copy the external address to the local address, and use the 
	tmp value from parse module to construct the dimensions for the branch
	true realization need some research
	'''
	if not (label in pySpice.global_data.NODE_TRANSLATION.keys()):
		pySpice.global_data.NODE_TRANSLATION[label] = node_dim
		node_dim += 1
		return node_dim-1, node_dim
	else:
		return pySpice.global_data.NODE_TRANSLATION[label], node_dim

def linear_generator(start, stop, step):
	temp = start
	if step > 0:
		while temp < stop:
			yield temp
			temp += step
	else:
		while temp > stop:
			yield temp
			temp += step

def dec_generator(start, stop, step):
	temp = start
	factor = pow(10, 1./step)
	while temp < stop:
		yield temp
		temp *= factor

def oct_generator(start, stop, step):
	temp = start
	factor = pow(8, 1./step)
	while temp < stop:
		yield temp
		temp *= factor
		
	
