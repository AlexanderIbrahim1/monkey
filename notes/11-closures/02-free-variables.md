# Compiling and Resolving Free Variables

Consider the following code snippet:
```
fn(a) {
    return fn(b) {
        a + b
    };
};
```

The inner function is the closure
- it references the argument `b` and the enclosing `a`

From the perspective of the inner function:
1. `a` is a free variable
  - so the compiler should emit an `OPGETFREE` to get it on the stack
2. `b` is an argument (local binding)
  - so the compiler should emit an `OPGETLOCAL` to get it on the stack

From the perspective of the outer function:
1. `a` is an argument
  - so the compiler should load it onto the stack with an `OPGETLOCAL`

Notice how the same variable is treated with a different opcode?


## How do we distinguish free and local variables?
We need to introduce a new scope; the `FREE` scope



## Quick overview of how free variables are treated
Suppose the compiler runs into an identifier
t needs to resolve the identifier, by calling the `resolve()` method on the current symbol table
1. if the compiler finds it (it is LOCAL, GLOBAL, BUILTIN, FREE), then that's that
  - if not, we need to go higher!
2. suppose we go to a higher scope's symbol table
  - suppose we find it
    - if the variable is in the GLOBAL or BUILTIN scope, then that's it, and we return it
    - but something different happens if it is in the FREE or LOCAL scope
3. if the variable in the higher scope is FREE:
  - if it was free in a higher scope, it has to be free in this scope too!
    - so we call `define_free()`, and add it to our special symbol table for this closure
4. if the variable in the higher scope is LOCAL:
  - that means the variable is LOCAL *to the higher scope*, but not LOCAL to the current scope
    - otherwise, we would have caught it in step (1)
  - so it must be free!!!

This is the process of how free variables are entered into the free symbols store
- the compiler tries to compile the variable, but finds out it is LOCAL or FREE to a higher scope
- that tells it to put the variable into a special store
  - it has to look up this value later!