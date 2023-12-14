# Chapter 07 - Functions

This chapter covers implementing functions and function calls in the compiler.

Some challenges:
1. functions are not *just* a series of instructions; they are first-class citizens!
  - we can pass functions around, and return them from other functions
  - how do we represent "instructions that can be passed around"?
2. how do we get the VM to execute the instructions of a function?
3. at the end of the function, how do we go back to where we left off?
4. how do we pass arguments to these functions?
  - how do the instructions fit into all that?


## Compiled Function Objects
Remember the roles of the compiler and VM:
1. compiler: turn the parsed "language components" into:
  - bytecode instructions
  - constants
2. VM: take the compiler's (bytecode instructions + constants), execute them

This has some implications for how we want to implement our functions:
We would rather not mix the instructions of the main program with those of the function
  - if we did, we would have to untangle them from the main instructions
  - SOLUTION: keep the instructions for the function separate from the main instructions
    - in their own compiled function object!

Remember that, in our parser, functions are represented as "function literals"
- they are constants!
- the sequence of instructions of a function does not change!

We can treat functions the same way in our compiler
- i.e. treat them as constants, and push them onto the stack of constant objects!

This is where we get the idea for "Compiled Function Objects"
- they are constants that hold the instructions that represent a function's execution!