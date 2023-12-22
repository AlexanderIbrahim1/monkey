# Built-in Functions

In our interpreter, we gave our language built-in functions.

## Review of Built-in Functions in the Interpreter
1. lex and parse the names of identifiers
2. check if the identifier is a built-in function (in a dictionary of built-ins)
 - this is done in the evaluator's `evaluate_identifier()` function
3. if it is, use the built-in function's evaluation


## Using Built-in Functions in our Compiler
As they are now, the built-in functions can't be easily used in our compiler
- they use internal references, make use of private helper functions, etc.
- not something we can easily implement in bytecode


## Possible Solutions

### Make compiler and VM depend on evaluator
This would allow us to directly use the built-in functions
However, this goes against the spirit of what we want to do (compile things!)

### Duplicate the definitions
We could give our compiler a different set of built-ins
However, this comes with the usual set of downsides of code duplication
(though I think it isn't as bad as the author makes it out to be)

### Move the built-ins to the object subpackage
The VM and compiler already depend on the object subpackage
- we already use lots of objects, like CompiledFunctionObject, etc.

This is the choice the author goes with
- it allows the interpreter to still use the same built-in functions
- it allows the VM and compiler to get access to them!