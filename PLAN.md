# Plan for monkey

## Creating an "executable binary"
I have completed the compiler and VM as described by the book.
So far, this is how it works:
- the lexer + parser: turn source code into statements and expressions
- the compiler: turn statements and expressions into `bytecode instructions` + `constants`
- the VM: take the `bytecode instructions` + `constants`, and run them

I want to create something similar to an executable
- have the compiler generate a file that I can carry around
- have the VM accept the file, and run it

### How to create this executable binary?
1. run the compiler until it creates the `bytecode instructions` + `constants`
2. use `pickle` to serialize the results
3. the VM will accept the file, deserialize the data, then run everything

I will also create a function that takes the serialized data, and prints it out in a nice format
- this is to show the user what the result of the compilation is