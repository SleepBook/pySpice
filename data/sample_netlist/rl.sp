test for the engine utility on linear circuit

*VS 1 0 1 AC 1 SIN(0 2 1K)
VS 1 0 1 AC 1 STAIR(0 2 6NS)
R1 1 2 2
L1 2 0 1u

.OP
*.AC LIN 10 1k 2k
.TRAN 1NS 3000NS
*.PRINT AC VM(2)
.PLOT TRAN V(2)
.END