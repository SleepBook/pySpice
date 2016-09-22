import matplotlib.pyplot as plt
import pdb

def plot(filename):
	f = open(filename,'r')
	filelines = f.readlines()
	f.close()
	seperator = []
	for i,line in enumerate(filelines):
		if line[0] == '*':
			seperator.append(i)

	analysis_num = len(seperator)/2
	for i in range(analysis_num):
		analysis_plot(filelines[seperator[2*i]:seperator[2*i+1]])
	raw_input('Press Any Character to Continue\n')
	plt.close()

def analysis_plot(section):
	"""
	current can only plot all into one graph
	"""
	analysis_type = section[1]
	if analysis_type == 'OPERATING POINT\n':
		return
	fig = plt.figure(analysis_type)
	scanbar = section[3].split()[1:]
	for line in section[4:]:
		if line == '\n':
			continue
		else:
			data = line.split()
			name = data[0]
			sub = plt.subplot()
			sub.plot(scanbar,data[1:],'o-')
	fig.show()

			
