# Closures

Closures are one of the more difficult features to include bytecode compilers and VMs

## Example
Consider the following code snippet:
```
00  let new_adder = fn(a) {
01      let adder = fn(b) {
02          return a + b;
03      };
04  
05      return adder;
06  };
07  
08  let add_two = new_adder(2);
09  add_two(3);  // 5
```

We create a closure called `adder` inside of the function `new_adder`

Why is it a closure?
- it doesn't just make use of its own parameter (`b`) or its own local bindings
- it accesses a parameter (`a`) defined in the enclosing function (`new_adder`)

When we write (`let add_two = new_adder(2);`):
- we get a specific version of the `adder` function that can still access the previous
  value of `a` passed to `new_adder` (in this case, `2`)


## Closures in Interpreters
Our interpreter could take the objects created by the parser and work with them directly
This made creating closures nearly trivial!
- we created an `Environment` type to pass into any function evaluation
- this `Environment` type holds the bindings from the outer scopes

The `Environment` type meant that functions *always* had access to the bindings of the
  scope in which those bindings were created
  - it didn't matter when they were created, and when we needed to use them; we had them!

The closure could simply "close over" the environment at the time of definition, and carry it around


## Closures in Compilers and VMs
Closures are much more difficult to implement in compilers and VMs

Remember that:
- the compiler turns the source code into bytecode instructions and constants
- the VM takes these bytecode instructions and constants, and runs them

So in the interpreter:
- the (1) creation of the `FunctionObject` and (2) closing over the environment
  happen at the same time

But in a compiler:
- the (1) creation of the `CompiledFunctionObject` happens during compilation
- the (2) environment only exists in the VM

### A more concrete example
Look at the code snippet earlier; notice that:
1. we have to compile the inner `adder` function into bytecode [lines 1-3]
2. we pass in the `2` into `new_adder` [line 8]

The compiler only knows that we have to push `2` onto the stack at some point
- it has no idea that the `2` will be bound to `a`

The VM *does* know that `2` will be bound to `a`
- but at this point it is too late to do anything about it!
- the `CompiledFunctionObject` has already been compiled!
  - it's already in the `globals` stack or the constants
  - it never got a chance to close over the `2`

So we need to give compiled functions the ability to reference bindings, even though
  these bindings are only given values after the function has already been compiled