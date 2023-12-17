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


## Nested Scopes
We implement local bindings by creating nested symbol scopes
- sort of like a linked list of symbol scopes

Each symbol scope has an `outer` field
- the global symbol scope pointers to nothing
- when a new symbol scope is created, it is given the current symbol scope as its `outer` field

1. if we enter a scope:
- we create a new symbol scope, and set the current symbol scope as its `outer` field
2. if we leave a scope:
- we set the current symbol scope to the symbol scope of the `outer` field