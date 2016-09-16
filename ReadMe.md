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
