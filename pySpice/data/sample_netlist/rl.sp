test for the engine utility on linear circuit

VS 1 0 1 AC 1 SIN(-1 1 1X)
*VS 1 0 1 AC 1 STAIR(0 2 6NS)
R1 1 2 2
L1 2 0 1u

.OP
.AC LIN 10 1k 2k
.TRAN 1NS 9000NS
.PRINT AC VM(2)
.PLOT TRAN V(2) I(VS)
.END