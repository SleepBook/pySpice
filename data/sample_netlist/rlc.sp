PASSED::tran RLC
VS 1 0 1 CONSTANT(0 1 1)
R1 1 2 1
L1 1 2 0.01n
C1 2 0 0.1N
.TRAN 0.01NS 0.5NS
.PLOT TRAN V(2)
.END