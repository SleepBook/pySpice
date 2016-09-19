import pySpice.global_data
import math
import cmath
import pdb

def format(sample, filename):
	"""
	Generate output text file through the raw watchlist data"""
	f = open(filename, 'w')
	f.write('*'*30)
	f.write('\n')
	f.write('OPERATING POINT\n')
	f.write('*'*30)
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
			f.write('*'*30)
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
						f.write('%f '%element)
				f.write('\n')
	f.close()
	return 0

def data_provider(analysis_type, cmd_list, watch_list, sample):
	"""
	Convert internal watch_list data into output print cmd data
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

	
