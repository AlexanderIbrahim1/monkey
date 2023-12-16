# Compiling Function Calls

We need to emit instructions that represent monkey's bytecode calling convention

For our bytecode, the convention is:
1. put the (compiled) function object you want on the call stack
2. VM executes the function's instructions
3. VM pops the function off the stack
4. if there is a return value, the VM puts that return value on the stack

This needs to work for both:
1. calling function literals directly after defining them:
```
fn() { return 2 + 4; }();
```
2. creating a function, binding it to a variable, and then calling that variable
```
let my_func = fn() { return 2 + 4; };
my_func();
```


## The calling convention is implicit
We are designing the calling convention such that
  we do *NOT* need to issue an `OPPOP` to get the function off the stack
This behaviour will be built into the VM


## The calling convention will change when we introduce arguments
This is why arguments haven't been mentioned yet
- we want to first cover the (much easier) case of compiling functions without arguments,
  before having to accommodate them


## The role of the VM
Let's go over what the VM does:

The bytecode's `constant` field can now contain instances of `CompiledFunctionObject`

As the VM loops over instructions, it will eventually hit an `OPCALL` instruction
1. this tells the VM to execute the instructions inside the `CompiledFunctionObject` on top of the stack
2. we do that until we reach an `OPRETURNVALUE` or an `OPRETURN` instruction
  - and remember that these returns will appear inside the `CompiledFunctionObject`'s instructions
3. we then remove the `CompiledFunctionObject` instance from the top of the stack
  - if there is a return value, we put it on top of the stack

### Keep the instruction pointer implementation
In the main loop, we loop over the instructions by incrementing the instruction pointer
- there are also jumps, etc.

We want to keep this mechanism!
- the only thing we want to change is the data we use the mechanism on
- we'll have an instruction pointer that goes over the instructions in the `CompiledFunctionObject`!


## Restoring old instruction pointers
We not only need to change the instruction pointers to enter scopes, but also change them back when we leave!
- and this won't just be one level; there might be nested levels to it!