single diode

*.TRAN 1NS 50NS
*.print tran v(2)
.OP

V1 1 0 DC -1 SIN(1 -1 25X)
D1 1 2 diode
RL 2 0 10

.END
