test for the engine utility on linear circuit

VS 1 0 1 AC 1 SIN(-1 1 1X)
R1 1 2 5
L1 3 0 1u
C1 2 3 1u

.OP
.AC LIN 10K 800K 1.2X
.TRAN 1NS 3000NS
.PRINT AC IM(VS)
.PLOT TRAN V(1) I(VS)
.END