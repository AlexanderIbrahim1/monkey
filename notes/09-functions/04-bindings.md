# Bindings

Our current monkey compiler supports only global bindings, but not local ones

Recall how this works:
- the VM has a stack called `globals`
1. when we encounter an `OPSETGLOBAL` instruction:
  - we pop the thing on top of the stack
  - we push it onto the stack of `globals` (or set it within the globals)
2. when we encounter an `OPGETGLOBAL` instruction:
  - we look it up in the `globals` stack (we *DON'T* pop it off)
  - we push it on top of the stack


## Local Bindings
Local bindings are those that are local to a function
- they are only visible and accessible within the scope of a function

### New Opcodes
We need to define opcodes that create and retrieve local bindings
- this will be very similar to what was done for global bindings

### Other details
The compiler needs to output these new opcodes correctly.
- must distinguish between local bindings and global bindings
- must distinguish between local bindings with the same name in different functions