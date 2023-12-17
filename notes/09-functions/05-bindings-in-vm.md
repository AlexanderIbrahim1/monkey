# Implementing Local Bindings in the VM

We need to be able to execute both `OPSETLOCAL` and `OPGETLOCAL` instructions
1. `OPSETLOCAL`:
- look at the thing on top of the stack, and pop it off
- bind it to a name
- store it in a *local* cache
2. `OPGETLOCAL`: 
- search up the name in the *local* cache
- put it on top of the stack


Some things we need to worry about:
- make sure the local bindings work at all
- what if there are multiple bindings in a single function?
- what if there are multiple bindings in multiple functions?
- what if two different functions each have a binding of the same name?


## How do we implement all this?
There author points out two ways to do this

### Using a data structure to hold nested bindings
Remember how we treated symbol scopes in the compiler?
- we have a symbol scope that holds an `outer` field, which (might) point to another symbol scope
- upon entering a scope, we create a new symbol scope that:
  - represents the current (nested) scope
  - holds a pointer to the parent scope, so we can return after leaving the scope

PROS:
- easy to implement (we've already done it once)

CONS:
- slow; we want the execution to be fast!
- we don't learn anything new

### Storing locals on the stack
We can just put the locals directly on the stack!
- after all, it is already the place where we store "data relevant to the current function"

CONS:
- more difficult to implement

PROS:
- faster
- more closely resembles what a lot of faster VMs do
  - this is how the stack is more commonly used anyways!


  
## How to use the stack for storing locals
Here is the strategy:

Suppose we come across an `OPCALL` instruction
1. we take the current value of the stack pointer, and store it for later use
2. we count the number of locals used by the function we are about to execute
  - we increase the stack pointer by this number
3. this empty space on the stack is where we will store the function's local variable

A really good benefit of this strategy?
- after we exit the function's scope, we can just reset the stack pointer
- we don't even need to clean up after ourselves!

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

``` AFTER MOVING THE STACK POINTER
             [               ]
             [               ]
stack_ptr -> [               ]
             [               ]    <- HOLE
             [               ]    <- HOLE
             [    FUNCTION   ]
             [ OTHER VALUE 2 ]
             [ OTHER VALUE 1 ]
```

``` WHAT WE USE THE SPACE FOR
             [               ]
             [               ]
stack_ptr -> [               ]
             [    LOCAL 2    ]
             [    LOCAL 1    ]
             [    FUNCTION   ]
             [ OTHER VALUE 2 ]
             [ OTHER VALUE 1 ]
```

How do we begin to implement this?
- the compiler knows how many locals there are!
  - we can easily pass this information to the VM
- we then need to keep track of the current stack pointer
  - we can store this information in our `StackFrame` data structure!
- the rest of it is bookkeeping (storing the stack pointer, restoring it, etc.)