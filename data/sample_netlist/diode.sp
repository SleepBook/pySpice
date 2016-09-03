single diode

.DC v1 0 1 0.01
.print dc v(2)

v1 1 0 dc 1 ac 1 0
D1 1 2 diode
RL 2 0 1k

.END
