test for the engine utility on linear circuit

*VS 1 0 1 AC 1 SIN(0 2 1K)
VS 1 0 1 AC 1 STAIR(0 2 6NS)
R1 1 2 1k
L1 2 0 0.1592

.OP
*.AC LIN 10 1k 2k
.TRAN 0.1NS 30NS
*.PRINT AC VM(2)
.PLOT TRAN V(1) V(2)
.END