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