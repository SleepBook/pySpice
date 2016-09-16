Test for dc sweep

VIN 1 0 2
R1 1 2 2
R2 2 0 4
R3 2 3 2
V2 3 0 2

.DC VIN 0 10 1
.PRINT DC V(2) V(1) V(3)
.END