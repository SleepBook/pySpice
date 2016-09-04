class ele_2port():
	def __init__(self,catagory,name,loc_p,loc_n,value):
		self.catagory = catagory
		self.name = name
		self.value = value
		self.loc_p = loc_p
		self.loc_n = loc_n
		self.branch_flag = 0
		self.active_flag = 0

class resistor(ele_2port):
	def __init__(self, *av):
		ele_2port.__init__(self, *av)
		self.ic = 0

class capacitor(ele_2port):
	def __init__(self, *av):
		ele_2port.__init__(self, *av)
		self.active_flag = 1

class inductor(ele_2port):
	def __init__(self, branch_num, *av):
		ele_2port.__init__(self, *av)
		self.branch = branch_num
		self.active_flag = 1
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
		self.active_flag = 1

class mos():
	def __init__(self, name, model, loc_d, loc_g, loc_s, loc_b):
		self.name = name
		self.model = model
		self.loc_d = loc_d
		self.loc_g = loc_g
		self.loc_s = loc_s
		self.loc_b = loc_b
		self.w = 0
		self.l = 0
		



class pulse_src():
	def __init__(self, vdd, vgnd, td, tr, tf, pw, per):
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


#below are the class for analysis cmds
class analysis_dc():
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
	def __init__(self, generator):
		self.catagory = 'tran'
		self.generator = generator
		self.uic_flag = 0
		self.show_start = 0
		self.max_step = 0

class print_item():
	def __init__(self,cmd):
		self.cmd = cmd
		self.op_flag = 0
		self.op_list = []
		
		
