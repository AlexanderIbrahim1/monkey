# Recursive Functions in the Compiler and VM

Consider the following code snippet, where `countdown()` is used recursively:
```
let wrapper = fn() {
    let countdown = fn(x) {
        puts(x);
        if (x > 0) {
            countdown(x - 1);
        }
    };
    return countdown(10);
};
wrapper();
```

What will happen when we try to compile this?
- we try to create the closure that gets bound to `wrapper`; let's skip ahead
- we try to create the closure that gets bound to `countdown`; let's skip ahead
- we load the argument (local binding) `x` onto the stack, then use it in `puts()`
- we check the condition of `x > 0`
- we want to call `countdown(x - 1)`

It is this last step that we are concerned with:
- we do the usual song and dance with the argument:
  - emit instructions to get `x` (locally) and `1` (constants), push them on the stack, subtract
- we prepare to deal with the call instruction
  - we find the identifier `countdown` and try to resolve it

That last part is the problem!
- we can't resolve it, because `countdown` hasn't been compiled yet!
  - so we weren't able to put it into any cache (`globals` or a symbol scope store)


## Solution to recursive problem?
Create a new opcode `OPCURRENTCLOSURE`
- the compiler will check if it is working with an identifier with the same name as the current function
- if so, it will go to the symbol table, and create an entry that maps the current function name to its appropriate index
  - so like a retroactive `OPSETLOCAL` or `OPSETGLOBAL`