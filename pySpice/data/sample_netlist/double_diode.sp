::double diode complex
VS 1 0 1 AC 1 SIN(0 10 300X)
D2 1 0 mymodel
R1 1 2 10
C1 2 0 0.2N
D1 2 0 mymodel
.TRAN 0.05NS 5NS
.PLOT TRAN I(vs) V(2)
.END