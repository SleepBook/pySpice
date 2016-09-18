single diode

.DC V1 1 2 0.1
.print dc v(2)
.OP

V1 1 0 DC 1
D1 1 2 diode
RL 2 0 10

.END
