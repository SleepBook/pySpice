::diode & C
VS 1 0 1 AC 1 SIN(0 10 300X)
C1 2 0 0.2N
D1 1 2 mymodel
.TRAN 0.05NS 5NS
.PLOT TRAN I(vs) V(2)
.END