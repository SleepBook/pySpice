test for the engine utility on linear circuit

VS 1 0 1 AC 1 SIN(0 2 1K)
R1 1 2 5
L1 3 0 1
C1 2 3 1

.AC LIN 10 1k 2k
.TRAN 1NS 10NS
.PRINT AC VM(3) VM(0)
.PLOT TRAN V(3)
.END