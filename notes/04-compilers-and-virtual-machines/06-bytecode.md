# Bytecode


## What is Bytecode?
When looking at real machines, the instructions came in the form of binary
- there was the opcode, and the rest of the instruction
- the instruction is loaded into the IR, and then decoded

In a virtual machine, the instructions come in the form of bytecode
- the same parts of an instruction for a real machine are present here too
 - i.e. there is an opcode followed by the arguments, all implemented inside the bytecode instruction

NOTE: look at page 23 of the compiler book

Bytecode isn't very readable in byte format, so we use mnemonics to make the opcodes readable
- for example, we can use 'PUSH', whereas the bytecode will represent that 'PUSH' in bytes


## Bytecode is very specific
There are lots of bytecode formats
- they are very diverse and specialized in form
- so going into the specific details right now isn't too helpful

Bytecode is a domain-specific language for a domain-specific virtual machine


## Bytecode can implement instructions not seen in real machines
For example, the Java Virtual Machine (JVM) has:
- `invokeinterface` (to invoke an interface method)
- `getstatic` (to get static field of a class)
- `new` (to create new instance of the specified class)

And these are implemented as bytecode instructions, not as functions in Java (as we would imagine them)
