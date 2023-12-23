# Closure Implementation

## New definition: free variable
A "free variable" is a variable seen in a function that is *not* any of the following:
- a variable with a global binding
- a variable with a local binding
- an argument to the function

So a free variable is used locally, but defined in an enclosing scope

Implementing closures with a VM and compiler revolves around using free variables


## Turn each function into a closure!
The book takes this approach: turn every function into a closure!

So actual functions are just closures that make no use of the closure's extra functionality

We create a `ClosureObject`
- it holds the `CompiledFunctionObject` that we want to run
- it also has a place to store the free variables it carries around and references