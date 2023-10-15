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


### Reminders
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

