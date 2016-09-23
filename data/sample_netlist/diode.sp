single diode

*.TRAN 1NS 100NS
*.print tran I(v1)
.OP

V1 1 0 DC 58.7785 SIN(-100 100 20X)
*V1 1 0 DC 200 STAIR(-200 200 12NS)
D1 2 1 diode
RL 2 0 10

.END
