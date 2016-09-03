PASSED::tran uic
VS 1 0 1
R1 1 2 1
C1 2 0 0.1N
.TRAN 0.005NS 0.7NS uic
.PLOT TRAN V(2)
.ic v(2)=0.5
.END