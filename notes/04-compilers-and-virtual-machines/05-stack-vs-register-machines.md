# Stack Machines vs Register Machines

We can split virtual machines into two categories: "stack machines" and "register machines"

In a virtual machine, there is a stack data structure, a program counter, and "memory"
- the stack will have memory pushed onto it as the machines

## Stack Machine
Suppose we get an instruction and decode it
- in a stack virtual machine, the operands of the instruction lie in the stack
 - so we read the operands from the stack, perform an operation, and push the new argument onto the stack

There are no (virtual) registers in a stack machine
- all our instructions operate directly on arguments that lie in the stack

## Register Machine
In a register machine, there are additional registers
- we can take things from the stack, and store them inside the registers


### The Pros and Cons?
Stack machines
- are "simpler" to build; they "only" make use of the stack
- require more "sub-instructions" per instruction; need to push and pop stuff off the stack repeatedly
- are generally slower (due to the extra pushing and popping)

Register machines
- are more complicated; there is an additional structure (the registers) to take care of
- require fewer "sub-instructions" per instruction; they can make use of registers directly
- are generally faster (less pushing and popping)


## An example of an architectural detail: dispatching
Suppose we get an instruction, look at its opcode, and decode it
- we then need to find out which "implementation" the instruction corresponds to [1]
- this is called "dispatching"

There are lots of ways to implement dispatching
- a switch statement is the most obvious, but gets slow if there are 100s of possible implementations
- some other options include:
 - jump tables
 - computed GOTO statements
 - indirect/direct threaded code

The goal is to minimize the amount of time it takes to "fetch + decode"; we want to focus on "execute"


### Side Nodes
[1] for example, is the instruction a PUSH, a POP, an ADD, a SUB, etc.
