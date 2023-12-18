# Arguments

Arguments to function calls are a special case of local bindings

Similarities:
- same lifespan (live until end of function)
- same scope (function scope)
- resolve the same way (look them up locally)

The only difference is their creation:
- local bindings are created by the user, explicitly, with a `let` statement
- arguments are implicitly bound to names, done behind the scenes by the compiler


## Where do we put arguments?
So far our calling convention is this:
- put the function you want to call onto the call stack (with `OPCONSTANT`)
  - then run `OPCALL`, and go through the body of the function
  - in the `OPCALL` instruction: we create a new frame, enter it, and advance the stack pointer
    to make space for the local bindings

So we made space for the local bindings, but what about the function arguments?
- where do we store them
  - where in memory space?
  - where in the calling convention?

### IDEA: put arguments on the stack
We're already using the stack for the local bindings; why not for the arguments?

NOTE: we put the arguments on the stack *before* advancing the stack pointer
- the book doesn't talk about this decision in a lot of detail
- but I guess it wouldn't matter if we made space on the stack for the arguments
  the same way we did for the local bindings
  - we would just have to do all the book-keeping somewhere else
  - i.e. `OPSETLOCAL` and `OPGETLOCAL` would have to perform shifts that account
    for the number of arguments on the stack

``` BEFORE
             [               ]
             [               ]
             [               ]
             [               ]
stack_ptr -> [               ]
             [    FUNCTION   ]
             [ OTHER VALUE 2 ]
             [ OTHER VALUE 1 ]
```

``` AFTER PUTTING ARGUMENTS ON STACK
             [               ]
             [               ]
             [               ]
             [               ]
stack_ptr -> [               ]
             [     ARG 2     ]
             [     ARG 1     ]
             [    FUNCTION   ]
             [ OTHER VALUE 2 ]
             [ OTHER VALUE 1 ]
```

``` AFTER EXECUTING OPCALL
             [               ]
             [               ]
stack_ptr -> [               ]
             [               ]  <- HOLE FOR LOCAL BINDING
             [               ]  <- HOLE FOR LOCAL BINDING
             [     ARG 2     ]
             [     ARG 1     ]
             [    FUNCTION   ]
             [ OTHER VALUE 2 ]
             [ OTHER VALUE 1 ]
```

PROBLEM:
- the `OPCALL` operation currently assumes the function is on top of the stack
- but now there are a bunch of arguments on top of the stack
  - how can `OPCALL` find the function to call?

SOLUTION:
- give `OPCALL` an operand, representing the number of arguments!