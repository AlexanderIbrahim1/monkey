# Chapter 03 - Evaluation

Evaluation is where interpreter implementations diverge the most
- we need to figure out what to do with the AST that our parser just gave us

Below we mention 3 common strategies, but there are so many more variations and strategies we could use


## Tree-walking Interpreters
The most obvious choice of what to do with the AST is to traverse it and interpret it
- visit each node
- do what the node signifies (print a string, add two numbers, etc.) on the fly


## Bytecode
Some interpreters first convert the AST into bytecode
- this is another intermediate representation (IR) of the AST

Usually, bytecode looks kind of like assembly: there are opcodes, push and pop for stack operations, etc.
- but bytecode is not assembly or machine code: the OS/CPU won't run it
- instead, a virtual machine runs the bytecode


## Just-in-time (JIT)
Some interpreters parse the source code, create an AST, and then turn that into bytecode
But the virtual machine doesn't execute the bytecode directly!
- instead, the virtual machine compilers the bytecode to machine code, just before it is executed
- this is calle da JIT interpreter/compiler


## Other Notes
Usually, when describing the difference between an interpreter and a compiler:
- an interpreter is something that doesn't leave executable artifacts behind
- a compiler is something that *does* create an executable

But the differences get fuzzy when looking at real-world implementations for real programming languages
