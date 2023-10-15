# Real Machines

Nearly all modern computers are built using the Von Neumann architecture; the parts include:
1. Processing Unit
- contains registers, an ALU, and other things
2. Control Unit
- contains IR and PC
3. memory (RAM)
4. mass storage
5. input/output

The combination of the "processing unit" and the "control unit" is called the CPU


## Instruction Cycle
The role of the CPU is to (1. fetch instruction from PC, 2. decode, 3. execute)
- somewhere in this process, the PC is updated (might be done after fetch, and possibly again after decode)

The combination of these three instructions is called a "cycle"


## Interplay between CPU and memory
The virtual machines involved in compilers mostly focus on the interplay between CPU and memory
- not much about I/O
- a bit about mass storage (OS typically handles that)


## Data and Program are stored in the same memory
The instructions, and the data they operate on, are both stored in memory (or mass storage)
- but they're often not stored in the same locations; they are separated into different regions

Memory can be separated into regions that store:
- data memory: memory that stores data (contents of a text file, variables, dynamic structures, etc.)
- instruction memory: memory that stored instructions to feed into the PC
- static data: data that doesn't change during execution
- dynamic data: data that changes during execution frequently (often in RAM)
- and others

For example, "instructions" only become instructions after the CPU fetches and successfully decodes them
- until then, it isn't distinguishable from memory representing anything else


## The call stack
There is a region of memory where the CPU accesses/stores data in a LIFO manner
- this is a specialized version of the stack, called a "call stack"

Why is there a call stack?
- the CPU needs to keep track of certain information to execute a program
- the most important pieces of information: the current instruction, and the next instruction

The elements that make up the call stack are called "stack frames"
- a stack frame contains information relevant to the current function being called; this includes:
 - the function's parameters and local variables
 - the return address (which instruction to go to next)
 - other, context-specific information about the function

### The Return Instruction
At the end of a function, there is a return instruction (return opcode)
- the specific implementation varies based on ISA

The return instructions for many ISAs do the following:
- pop the current function's stack frame off the call stack
- restore CPU registers to what they were before the function was called
- updates the PC with the return address stored in the stack frame


## Why a stack over other data structures?
A stack is ideal for storing information about where to jump to in "instruction space"
1. function calls are almost always nested
 - when we enter a function, we jump somewhere else, and when we finish, we return where we left off
 - the stack is an ideal way to represent this:
  - jump to another instruction = push onto the frame
  - return where we left off = pop off the frame
2. when inside a function, usually, all we need are the parameters and local variables
 - and this information is ideally stored within a stack frame!
 - so we only need to look at the top of the call stack!


## A Virtual Stack
For our virtual machine, we are going to implement our own call stack
- we will create stack frame objects in our backend programming language
- there will be registers, opcodes, and everything!


## Registers
While inside a function, the CPU needs to access the local variables and parameters
- but although accessing RAM is relatively fast, we can go even faster!
- this is where registers come in

The CPU has a collection of processor registers
- some are special registers, some are general-purpose registers (GPRs)
- they are much faster to access than RAM

Unfortunately, there often aren't that many registers
- EXAMPLE: in the x86-64 architecture, there are 16 GPRs, each 8 bytes large

Thus we only want ot use registers for small, frequently-accessed data

Some examples:
1. if we wanted to add 2 integers:
 - we load both of them into designated registers
 - we perform an instruction, and write the result into a third register!
2. if there is a large piece of data we access frequently, but can't store in a register
 - we can still store the *address* of that data in a register!

### Stack Register
There is a special register that points to the top of the stack
- it is used *incredibly frequently*



## Other Information

### Terminology Reminders
program counter: value that indicates where in memory the next instruction is
- literally just a number representing the virtualized address space
- a variety of mechanisms are then used to take this value and get the physical address space

word: smallest addressable region of memory
- this is a CPU-dependent value
- most modern computers use either 32-bit or 64-bit words


### Byte-Addressing
Consider 32-bit x86 processors (x86 = family of CISC ISAs developed by Intel)
1. they address memory in 8-bit (byte) units
2. they have 32-bit GP registers: thus can operate on 32-bit items with a single instruction
- they are considered byte-addressible
 - so what matters is how memory is addressible, not the register size, when defining them


### ISA and assembly instructions
An ISA defines the interface between hardware and software
- it provides:
 - the set of instructions that a CPU can execute
 - the available registers, addressing modes, etc.

This means that: different hardware design -> different ISA
- the available instructions depend on the hardware; a different hardware design could mean:
 - different organization of the instruction pipeline
 - different numbers and types of registers
 - different memory heirarchy
 - different word size
- the available instructions, registers, etc. are sensitive to these details
