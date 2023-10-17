# Constant Expressions

We have defined an `Instructions` type and an `Opcode` type, both using `bytes`

The first thing the book wants to do is create an opcode to push things onto the stack
- but the author mentions that this opcode:
 1. won't be solely about pushing things
 2. won't have "push" in its name

They talk about how it would be unwieldy to implement a `push` opcode for lots of different types


## The idea of "constants"
A "constant expression" (constant) is an expression that can be determined at compile time

```
  LEXER ----> PARSER ----> COMPILER ----> VIRTUAL MACHINE
|                                   |   |                 |
+--------- COMPILE TIME ------------+   +--- RUN TIME ----+
```

### Referencing constants in our instructions
The compiler can find these expressions in the code and store what they evaluate to
- this means we don't have to embed the values themselves in the instructions
- we can just embed the references to those values in the instructions
 - this "reference" will just be an integer (used to index a data structure that holds the value)

For example, suppose we run into an integer literal during compilation
- we evaluate it
- we store it in a data structure, and assign it an index (a number)
- we create an instruction that stores the index
- after compilation, we give the instructions + constant data structure to the VM
- the VM will use the index in the instruction to get the constant from the data structure
