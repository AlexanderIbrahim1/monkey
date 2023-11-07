# Keeping Track of Names

In this chapter, the book goes over implementing "bindings"
- adding support for let statements and identifier expressions

What would we have to do?
- need to compile let statements into bytecode
- need to compile identifiers into bytecode
- need an opcode to tell the VM to bind a value to an identifier
- need an opcode to tell the VM to retrieve a value bound to an identifier

Binding values to identifiers in a compiler is more difficult than in an interpreter
- our interpreter had a dictionary that used identifiers as keys, and we could easily pass
  around this dictionary
- but with a compiler, everything is stored linearly in bytecode; we can't just pass things around!

## Binding values to identifiers
This part is easier
1. push the value onto the stack
2. tell the VM to bind the topmost stack element to an identifier

## Representing Identifiers
Identifiers will just be represented as numbers
- for example, consider the following code:
```
let x = 33;
let y = 66;
let z = x + y;
```
- in this example, we would assign `0` to `x`, `1` to `y`, and `2` to `z`, and so on

We will have two new opcodes to help us:
1. `OPSETGLOBAL`: what we emit when compiling a let statement
2. `OPGETGLOBAL`: what we emit to retrieve a value
- both will have a single operand, 2 bytes wide, allowing for 65536 total bindings (more than enough)


### Example
Here's what the above three let statements would look like:
```
                        // let x = 33;
OPCONSTANT 0            // load '33' onto the stack
OPSETGLOBAL 0           // bind value on top of the stack to '0'

                        // let y = 33;
OPCONSTANT 1            // load '66' onto the stack
OPSETGLOBAL 1           // bind value on top of the stack to '1'

                        // let z = x + y;
OPGETGLOBAL 1           // push the global bound to 1 (the '66')
OPGETGLOBAL 0           // push the global bound to 0 (the '33')
OPADD                   // add them together to create '99'; load '99' onto the stack
OPSETGLOBAL 2           // bind value on top of the stack to '2'
```