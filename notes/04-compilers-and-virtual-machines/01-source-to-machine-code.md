# Life cycle of source code to machine code

Let's assume that we want to create a compiler that turns the monkey language into "machine code" [**]
- what does this process entail?

[**] We won't actually be writing a compiler that turns the code into machine code; we'll be turning it
     into something else

```
         [SOURCE CODE]
               |
               V
        (Lexer & Parser)
               |
               V
             [AST]
               |
---------------------------------
               |
               V
          (Optimizer)
               |
               V
    [Internal Representation]
               |
---------------------------------
               |
               V
        (Code Generator)
               |
               V
         [Machine Code]
```


## Lexer & Parser
We already have the "Lexer & Parser" part that turns source code into an AST
- we'll just reuse what we wrote from the material in the first book


## Optimizer
Next, there is an optional "Optimizer"
- this tool translates the AST into another data structure called the Internal Representation (IR)
- the IR might lend itself better to optimizations/translations than the AST
- i.e. the optimizer just changes the AST into something easier for the "Code Generator" to work with

This IR might go through several optimization phases; some examples:
- eliminate dead code
- pre-calculate simple math
- remove code from body of loop that doesn't have to be inside it, etc.


## Code Generator
The "Code Generator" (also called the "backend") takes the IR, and turns it into the target language


## What isn't shown
This is only how the "simplest" compilers work; there are 1000s of possible variations
- the optimizer might do multiple passes over the IR (different optimizations in each pass)
- or maybe there is no optimizer, and the code generator works directly with the AST
- or maybe it doesn't create machine code, but another type of code (like LLVM IR)
- or maybe there are multiple optimizers, backends, etc. for different architectures

The only thing that connects all these different possibilities, is the idea of translation
- to take source code in one language, and generate source code in another language
