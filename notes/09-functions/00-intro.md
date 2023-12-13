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