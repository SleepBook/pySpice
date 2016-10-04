import pySpice.global_data
import math
import cmath
import pdb

def format(sample, filename):
	"""
	Generate Text Output

	:param sample: the output of the solve function, a python dictionary containing the status of the point apperaed on watch_list
	:param filename: a string specify the output filename
	:return: will write a text file containing the result for the analysis. The format illustrate itself best through an example.

	"""
	f = open(filename, 'w')
	f.write('*'*30)
	f.write('\n')
	f.write('OPERATING POINT\n')
	f.write('-'*30)
	f.write('\n')
	for key in pySpice.global_data.NODE_TRANSLATION.keys():
		f.write(key + ' ')
	f.write('\n')
	for index in pySpice.global_data.NODE_TRANSLATION.values():
		f.write('%f '%pySpice.global_data.INIT_STATE[index])
	f.write('\n')
	f.write('*'*30)
	f.write('\n')
	f.write('\n')
	f.write('\n')	

	for item in pySpice.global_data.ANALYSIS_LIST:
		if item == 1:
			continue
		else:
			analysis_type = item.catagory
			f.write('*'*30)
			f.write('\n')
			if analysis_type == 'ac':
				f.write('AC ANALYSIS\n')
			elif analysis_type == 'dc':
				f.write('DC SWEEP\n')
			elif analysis_type == 'tran':
				f.write('TRANSIENT ANALYSIS\n')
			f.write('-'*30)
			f.write('\n')

			output = data_provider(
				analysis_type,
				pySpice.global_data.PRINT_DICT[analysis_type],
				pySpice.global_data.watch_list[analysis_type],
				sample[analysis_type])

			for line in output:
				for i,element in enumerate(line):
					if i == 0:
						f.write(element+' ')
					else:
						if abs(element) < 1e03 and abs(element) > 1e-03:
							f.write('%4f '%element)
						else:
							f.write('%.3e '%element)
				f.write('\n')
			f.write('*'*30)
			f.write('\n')
			f.write('\n')
			f.write('\n')
	f.close()
	return 0

def data_provider(analysis_type, cmd_list, watch_list, sample):
	"""
	Generating the Data for PRINT/PLOT Commands Using the Raw Data of the Status of the Points/Branches to watch_list

	Also it re-arrange the data layout. So in the finally output, the first line is the sweep item. Following lines begins with the PRINT/PLOT item's name and then it's values in consecutive sweep points.

	:param analysis_type: either 'ac' 'dc' or 'tran'
	:param cmd_list: a list containing  the print/plot items for this analysis
	:param watch_list: the watch_list, stating which points/branches are of interest
	:param sample: the output of *solve()* function
	:return: an list *output* containing the information for the values of the item appeared in the PRINT/PLOT commands.
	"""
	output = []
	if analysis_type == 'dc' or analysis_type == 'tran':
		scan_bar = sample[-1][:]
		scan_bar.insert(0,'scanbar')
		output.append(scan_bar)
		for item in cmd_list:
			output_slice = []
			output_slice.append(item.cmd)
			if item.op_flag == 1:
				index_p = watch_list.index(item.op_list[0])
				index_n = watch_list.index(item.op_list[1])
				for i in range(len(sample[-1])):
					output_slice.append(sample[index_p][i] - sample[index_n][i])
			else:
				index = watch_list.index(item.op_list[0])
				for i in range(len(sample[-1])):
					output_slice.append(sample[index][i])
			output.append(output_slice)

	elif analysis_type == 'ac':
		scan_bar = sample[-1][:]
		scan_bar.insert(0,'scanbar')
		output.append(scan_bar)
		for item in cmd_list:
			output_slice = []
			output_slice.append(item.cmd)
			if item.op_flag == 1:
				index_p = watch_list.index(item.op_list[0])
				index_n = watch_list.index(item.op_list[1])
				if item.cmd[1] == 'r':
					for i in range(len(sample[-1])):
						output_slice.append(sample[index_p][i].real - sample[index_n][i].real)
				elif item.cmd[1] == 'i':
					for i in range(len(sample[-1])):
						output_slice.append(sample[index_p][i].imag - sample[index_n][i].imag)
				elif item.cmd[1] == 'm':
					for i in range(len(sample[-1])):
						output_slice.append(abs(sample[index_p][i]) - abs(sample[index_n][i]))
				elif item.cmd[1] == 'p':
					for i in range(len(sample[-1])):
						output_slice.append((cmath.phase(sample[index_p][i]) - cmath.phase(sample[index_n][i]))* 180/cmath.pi)

			elif item.op_flag == 0:
				index = watch_list.index(item.op_list[0])
				if item.cmd[1] == 'r':
					for i in range(len(sample[-1])):
						output_slice.append(sample[index][i].real)
				elif item.cmd[1] == 'i':
					for i in range(len(sample[-1])):
						output_slice.append(sample[index][i].imag)
				elif item.cmd[1] == 'm':
					for i in range(len(sample[-1])):
						output_slice.append(abs(sample[index][i]))
				elif item.cmd[1] == 'p':
					for i in range(len(sample[-1])):
						output_slice.append(cmath.phase(sample[index][i])*180/cmath.pi)
			output.append(output_slice)

	return output

	
