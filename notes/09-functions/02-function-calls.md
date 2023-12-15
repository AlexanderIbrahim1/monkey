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