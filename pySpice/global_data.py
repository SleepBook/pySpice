"""
Global Data Structure

This Structure will be used all over the program, so I set them as global data structure. The part above the pound key dividing line is the structure container of the internal representation of the circuit. Below the dividing line is some parameter regarding the MOSFET, DIODE parameters

:MNA_dim: the dimension of the MNA matrix
:ELEMENT_DICT: a python dictionary containing the instances of the circuit elements, with their name as index
:SETTING_LIST: list containing the setting commands of SPICE
:ANALYSIS_LIST: list comtaining the analysis commands, which are parsed into special designed class instance
:PRINT_DICT: PRINT/PLOT commands in SPICE are parsed specially as the instance of the print_item class. These instances are put into respective list of this dictionary.
:watch_list: A list log the name(interanl) of the nodes/branches of intereset.
:INIT_STATE: This list is used to override the result of the .OP command if .IC command is specified.
"""
MNA_dim = 0

ELEMENT_DICT = {}
SETTING_LIST = []
ANALYSIS_LIST = []
PRINT_DICT = {'dc':[], 'ac':[], 'tran':[]}
watch_list = {'dc':[], 'ac':[], 'tran':[]}

NODE_TRANSLATION = {'0':0}

INIT_STATE = []

CONVERGE_CRITERIA = 0.0000001
#####################################
#DEVICE PARAMETER BELOW COME FROM 
#DIC Rabaey P.103
K_NMOS = 1.15*1e-04
K_PMOS = 0-3*1e-05
LAMDA_NMOS = 0.06
LAMDA_PMOS = 0 - 0.1
VTH_NMOS = 0.43
VTH_PMOS = 0 - 0.4
#####################################
