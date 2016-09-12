test for the engine utility on linear circuit

VS 1 0 1 SIN(0 2 1K)
R1 1 2 5
L1 3 0 1m
C1 2 3 1

.AC LIN 200 1k 2k
.TRAN 0.01NS 1NS
.PLOT TRAN V(3)
.END