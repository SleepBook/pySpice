test for the engine utility on linear circuit

VS 1 0 1 AC 1 SIN(0 2 1K)
R1 1 2 1k
L1 2 0 0.1592

.AC LIN 10 1k 2k
.TRAN 0.01NS 1NS
.PRINT AC VM(2)
.PLOT TRAN V(2)
.END