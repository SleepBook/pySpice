"""Global Used Data Structure"""
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