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