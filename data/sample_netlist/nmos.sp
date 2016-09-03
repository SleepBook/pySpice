:: single nmos
VIN 3 0 1.8 constant (1.8)
VDD 1 0 1.8 constant (1.8)
M1 2 3 0 0 NMOS L=2U W=2U
R1 1 2 57.97K
.TRAN 0.05NS 5NS
.PLOT TRAN V(2) I(VDD)
.END