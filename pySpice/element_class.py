"""
These classes works more like C Structure. It stores the information of the circuit element or SPICE commands into its different fields.
"""

class ele_2port():
	"""
	Base class for most dual-port circuit elements

	:member:
		+ catagory: describing what kind of device this instance belong to
		+ loc_p: Positive port in internal representation(an integer)
		+ branch_flag: whether this element need a variable to represent the current throught it.
	"""

	def __init__(self,catagory,name,loc_p,loc_n,value):
		self.catagory = catagory
		self.name = name
		self.value = value
		self.loc_p = loc_p
		self.loc_n = loc_n
		self.branch_flag = 0
		
class resistor(ele_2port):
	def __init__(self, *av):
		ele_2port.__init__(self, *av)
		self.ic = 0

class capacitor(ele_2port):
	def __init__(self, *av):
		ele_2port.__init__(self, *av)

class inductor(ele_2port):
	"""
	:member:
		+ branch: the internal variable represent the current throught it
	"""
	def __init__(self, branch_num, *av):
		ele_2port.__init__(self, *av)
		self.branch = branch_num
		self.branch_flag = 1

class i_src(ele_2port):
	def __init__(self, *av):
		ele_2port.__init__(self, *av)
		self.ac = 0 + 0j
		self.tran = 0

class v_src(ele_2port):
	def __init__(self, brch_num, *av):
		ele_2port.__init__(self, *av)
		self.branch = brch_num
		self.branch_flag = 1
		self.ac = 0 + 0j
		self.tran = 0

class vcvs(ele_2port):
	def __init__(self, loc_ctrl_p, loc_ctrl_n, brch_num, *av):
		ele_2port.__init__(self, *av)
		self.loc_ctrl_p = loc_ctrl_p
		self.loc_ctrl_n = loc_ctrl_n
		self.branch = brch_num
		self.branch_flag = 1

class vccs(ele_2port):
	def __init__(self, loc_ctrl_p, loc_ctrl_n, *av):
		ele_2port.__init__(self, *av)
		self.loc_ctrl_n = loc_ctrl_n
		self.loc_ctrl_p = loc_ctrl_p

class cccs(ele_2port):
	def __init__(self, loc_ctrl_brch, *av):
		ele_2port.__init__(self, *av)
		self.loc_ctrl_branch = loc_ctrl_brch
		self.branch_flag = 1

class ccvs(ele_2port):
	def __init__(self, brch_num, loc_ctrl_brch, *av):
		ele_2port.__init__(self, *av)
		self.loc_ctrl_branch = loc_ctrl_brch
		self.branch = brch_num
		self.branch_flag = 1

class diode(ele_2port):
	def __init__(self, model, *av):
		ele_2port.__init__(self, *av)
		self.model = model
		self.ic = 0

class mos():
	def __init__(self, name, model, loc_d, loc_g, loc_s, loc_b):
		self.catagory = 'mos'
		self.name = name
		self.model = model
		self.loc_d = loc_d
		self.loc_g = loc_g
		self.loc_s = loc_s
		self.loc_b = loc_b
		self.w = 0
		self.l = 0
		self.branch_flag = 0

class pulse_src():
	""" 
	The meaning of these fields refer to this graph:

	.. figure:: ../figures/SPICE_pulse.png
	"""
	def __init__(self, vgnd, vdd, td, tr, tf, pw, per):
		self.catagory = 'pulse'
		self.vdd = vdd
		self.vgnd = vgnd
		self.td = td
		self.tr = tr
		self.tf = tf
		self.pw = pw
		self.per = per

class exp_src():
	def __init__(self):
		pass

class sin_src():
	def __init__(self, vdd, vgnd, freq):
		self.catagory = 'sin'
		self.vdd = vdd
		self.vgnd = vgnd
		self.freq = freq

class stair_src():
	def __init__(self, vgnd, vdd, up_moment):
		self.catagory = 'stair'
		self.vdd = vdd
		self.vgnd = vgnd
		self.up_moment = up_moment


#below are the class for analysis cmds
class analysis_dc():
	"""
	:member:
		+ swp_src: the value of the sweep points are put into a generator
	"""
	def __init__(self, swp_src, generator):
		self.catagory = 'dc'
		self.swp_src = swp_src
		self.generator = generator
		self.double_scan_flag = 0
		self.swp_src2 = ''
		self.generator2 = 0 #run into this case from time to time, how to resolve?

class analysis_ac():
	def __init__(self, generator):
		self.catagory = 'ac'
		self.generator = generator

class analysis_tran():
	def __init__(self, generator, step):
		self.catagory = 'tran'
		self.generator = generator
		self.step = step
		self.uic_flag = 0
		self.show_start = 0
		self.max_step = 0

class print_item():
	"""
	The PRINT/PLOT commands are parsed to the instance of this class

	:member:
		+ cmd: the original string describing the plot/print
		+ ac_flag: whether it's an AC plot, because the print/plot command to AC need special process(they have another character noting to plot magnitude, phase or anything else
		+ op_flag: some plot need to calculate the difference between two nodes. If so, this flag is setted.
		+ op_list: document which two nodes need to do opeeration on
	"""
	def __init__(self,cmd):
		self.cmd = cmd
		self.ac_flag = 0
		self.op_flag = 0
		self.op_list = []

class sweep_item():
	"""
	The standard information package the stamp function pass to the engine module. Control the behavior of the engine

	:member:
		+ switch: a string either of 'gen' or 'upd'. If 'gen' it tells the engine in each iteration the new stamp value come from a generator. Otherwise, the value get its update from the solution of previous iteration
		+ coord: where the new stamp fit in
		+ generator: the generator to offer the new value
		+ updata_src: the coordinate where to retrieve the updata value
	"""

	def __init__(self, switch, coord):
		self.switch = switch
		self.coord = coord
		self.generator = 0
		self.update_src = 0
		
		
