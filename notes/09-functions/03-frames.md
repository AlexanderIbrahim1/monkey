# Stack Frames

Stack frames are how we keep track of the instruction pointers and data as we enter or leave scopes

A frame ('stack frame' or 'call frame') is a data structure that holds all "execution-relevant information"
NOTE: in compiler literature, this is sometimes called an "activation record"


## Stack frames on real machines
On a real machine, a stack frame is used to store lots of things!
- the return address
- the arguments to the current function
- the local variables of the current function
- the stack pointer, etc.

Designers of real machines are constrained by things like "real memory" and "standardized calling conventions"
- these add lots of complications and restrictions


## Stack frames on virtual machines
VMs aren't bound by the same constraints that real machines are
- we can store whatever execution-relevant information on a stack frame that we want!

There are lots of different choices, and they differ greatly between VMs
- some keep only the return address
- some also have the local variables
- some also have the arguments to the function call, etc.

There are trade-offs between performance, ease-of-implementation, etc.


## Stack frames in our Monkey compiler
For now, a stack frame in our compiler will contain:
- the entire `CompiledFunctionObject`
- an instruction pointer for that stack frame