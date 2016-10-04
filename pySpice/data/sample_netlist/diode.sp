single diode

.TRAN 1NS 100NS
.print tran v(2)
.OP

V1 1 0 DC 58.7785 SIN(-100 100 20X)
*V1 1 0 DC 200 STAIR(-200 200 14NS)
D1 1 2 diode
RL 2 0 10

.END
