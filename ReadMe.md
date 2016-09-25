#DEVELOPING NOTES

## Parser Part
***this part parse the spice netlist to internal representation***

the general woring flow is do a single-pass parse, and store the
information all in designed classes(working like structure here, because
the possess no methods)

the circuit conponent are put into the ELEMENT_DICT dictionary, with the
element's name as key and a respective object as value(rationale for
using dict rather than list is for easy finding when translation)

setting cmds like, *.nodeset*, *.ic* etc are put into SETTING list.

analysis cmd(.dc, .ac, .tran) are put into ANALYSIS_LIST list, these
cmds are parsed also as objs, these objs, and the scanning list are
created as python generator for later easy use and efficient memory
purpose.

While parsing, the dictionary of NODE_TRANSLATION are also setup along
the way, this dict hash the node name(and element's name, which will
cause a branch in the MNA matrix) to the intenal node
representation(essentially the MNA matrix's row number)

.print/.plot cmds are parsed specially into and dict PRINT_DICT, each
obervation are abstracted into an instance of the class print_item, this
class basiclly contains the information of what this print is, which
internal node need to observe and how to generate the final value based
on the obserbed internal node value.<br>
***ATTENTION***<br>
actually in this part i encountered some puzzle: at my original design
of the class print_item, all the internal observed point be put into a
list called *op_list*, and how to generate the final output data are
also somehow stored to this particular object( i did so because at first
i think how to generate the output can varied much from case to case,
thus to me a cleaner way to do so is formulate the algorithm when
parsing and attach this to the object, so when using, the user direct
invoke this 'func' and will get the output he want) they way i can think
of doing so is to use functional programming feature provided by
python(pass a func as an parameter), use overload of a class method
should also do the trick. BUt i wonder what's teh professional way to
realize this functionality. <br>
(current even not realize, because i found in most cased doing op2 - op1
 is enough)


finally, a second-pass is necessary, because in first-pass someplace
still use external node name(print) and the node name and branch name
are not named contiously.(translate_dict), these job are assigned to the


##Inductor AC Resolution

in AC analysis, the branch reserved for inductor is no longer needed.
However, changing the MNA structure and re assign number to the element
in the MNA is time-consuming. Here the resolution i came up with is to
change the AC stamping for the inductor a bit:

that's in the p_port line and n_port line only stamp 1 and -1 in the
branch coloum respectively. And in the coloum line stamp how to
calculate the current through the inductor by the volatge on it's side.

This implement can be account in two ways. First, it can be seen as
elaborate the involve an abundunt varible: the current through the
inductor and add an extra equivilance for it. The other way is simply
see it as a transformation of the original matrix. In fact, the matrix
at hand can easily be deduced to the original MNA.
internalize function


##Add MOSFET SUPPORT and Test pesudo-NMOS Inverter

actually this step takes more time than it should do. 

THe main reason is i forget too much about the mosfet, however, i pick it up and want to summarize it here:

while, the drain current(plus if current flow into drain to source, this is actaully import when you analysis PMOS), is a bivarient function of Vgs and Vds. So, when linarize its behavior to fit into lienar function, it will be affeted by both varible. 

actually, the mistake i made is want to think the influence of all the two varible at once, likethe Id is somehow a curve in the space, and Vds and Vgs are x and y axis respectively. however, this attemption turned out to be a little difficult and fruitless when you actually do analysis.a better way is find is just think $$Id = Gm*Vgs + Gds*Vds + bias$$, and the behavior of a mosfet is no different than two coupled resistors, the even better new is that, in most cases, you dont't need to consider all the two transistor at once, in these case, the behavior of MOSFET is simple a resistor.

Under this perspective, you may sumarize the behavior of MOSFET as below:
in linear region, if Vgs remain unchanged, to Vds, the mosfet is just like a resistor with small resistance. This character is utlized in the Inverter. that's when Vgs is high(the higher Vgs is, the smaller the resistance is to Vds), will attach a big resistor between drain and vdd, and pull the voltage at drain near ground. The reason the inverter should work at this region is to utlize the small resistance between drain and source when the mosfet in linear region.

since i just finished the inverter, i want to say a couple more words: the design of an inverter is actually like this:(you can refer to the inverter.png) when you expand the mosfet at some point in the linear region, it's behavior is like a transistor which is represented by the red line. you need to attach a resistor from drain to vdd, which beahvor is represent by the blue line, the intersection is the final voltage of drain. of course you want this voltage to be as low as possible, which is equal to make the slope of the blue line as low as possible. In this Id-Vgs graph, that means a bigger transistor. (also, to the extreme, you do not attach any resistor at all, and that's the behavior of the vertical gray line, in that case, the Voltage of drain is equal to vdd)

in quantative analysis, in .25 technology from rebaey's book, given the vdd of 1.8v the resistance of the mosfet in linear region is around 10K Ohm, so you may want to attach a resistor of at least 100k Ohm.


Similarly, in linear region, if Vgs unchanged, the equal admitance(or transcoductance, to be exact) of Vds is extreme low, that means, no matter how great you imporve hte vgs, the Id barely increase.

In Staurate region, when Vds unchanged(or always bigger than Vgs-Vth), the transconductance of Vgs is extreme high, this charactre is used to design amplifer.

In Saturare region, when Vgs unchanged, the admitance of Vds is extremen high, this characterr is used to generate extremen large dynamic resistance. actually, thatis the trick of CMOS Inverter.
