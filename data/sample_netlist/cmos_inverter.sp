cmos inverter

VIN 1 0 0 PULSE(0 1.8 0NS 10NS 10NS 10NS 40NS)
M1 2 1 0 0 NMOS L=2U W=2U
M2 2 1 3 3 PMOS L=2U W=2U
VDD 3 0 1.8 STAIR(0 1.8 0NS)

.OP
*.TRAN 1NS 80NS
*.PLOT TRAN V(2) V(1)
.END