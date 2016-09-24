test for the engine utility on linear circuit

VS 1 0 1 AC 14 SIN(-1 1 1X)
*VS 1 0 1 AC 1 PULSE(0 2 0 0 0 100NS 120NS)
*VS 1 0 1 AC 1 STAIR(0 2 6NS)
R1 1 2 1m
C1 2 0 1m

.OP
.AC DEC 10 1 1X
*.TRAN 1NS 9000NS
.PRINT AC VM(2)
*.PLOT TRAN V(2) I(VS)
.END