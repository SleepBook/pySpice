test for the engine utility on linear circuit

*VS 1 0 1 AC 1 SIN(0 2 50X)
*VS 1 0 1 AC 1 PULSE(0 2 0 0 0 100NS 120NS)
VS 1 0 1 AC 1 STAIR(0 2 6NS)
R1 1 2 5
C1 2 0 1N

.OP
*.AC LIN 10 1k 2k
.TRAN 0.1NS 15NS
*.PRINT AC VM(2)
.PLOT TRAN V(1) V(2)
.END