# Opcodes to Execute Functions

What new opcodes do we need to implement the compilation and execution of functions?

## What opcodes *DON'T* we need?
We DO NOT need an opcode for function literals
- functions are compiled into `CompiledFunctionObject` instances
  - these are treated as constants
  - they are loaded on the VM's stack using the `OpConstant` instruction

We DO NOT need an opcode for binding functions to names
- we can already do that with `let` statements (and with `OpSetGlobal` and `OpGetGlobal`)


## What opcodes *DO* we need?
We need an opcode for evaluating a function call
- we'll start small, assuming a function that takes no arguments and returns no arguments
- we'll eventually add the ability to accept and return values


### OPCALL
`OPCALL` is the opcode we introduce for implementing function calls

How is it used?
1. we use a different instruction to get "the function we want to call" on the stack
  - probably an `OPCONSTANT` instruction
2. we issue an `OPCALL` instruction
  - it tells the VM to execute the function on top of the stack

Because this instruction *always* refers to the function object on top of the stack,
  we don't need to have an operand

### OPRETURNVALUE
`OPRETURNVALUE` is the opcode we introduce for returning values

Remember that the Monkey language allows for both implicit and explicit returning of values
```
fn() { 5 + 10 }
fn() { return 5 + 10; }
```
- conveniently, both of these will compile to the same bytecode instructions!

How is it used?
1. we compile the return value
2. we issue an `OPRETURNVALUE` instruction
  - it tells the VM to put that value on top of the stack

Because this instruction *always* refers to the object on top of the stack,
  we don't need to have an operand

### OPRETURN
`OPRETURN` is the opcode we introduce for "returning from a function" that returns nothing
- i.e. it is just for returning the control flow to whatever we were doing before the function

This instruction doesn't even refer to anything, so we don't need to have an operand