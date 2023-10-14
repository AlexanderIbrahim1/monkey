# Compilers and Virtual Machines

The words "interpreter", "compiler", and "virtual machine" can each refer to many different things
- because there are so many variations and so many details, the lines can get blurred


## Definition of Compiler
The definition of a compiler that the book shows us:
```
A compiler is computer software that transforms computer code written in one
programming language (the source language) into another computer language (the
target language).
```

So a computer is a translator of programming langauges
- for most cases we think about, the "target language" is machine code, giving us an executable


## Interpreters vs Compilers

An interpreter and compiler both involve taking source code, putting it through a lexer and a parser,
and then doing something with the parsed expressions and statements
- an interpreter (typically) does not create an executable image
 - it just executes the expression and statements directly
- a compiler creates an executable image

Another way to put it:
- an interpreter will interpret the language directly
- a compiler will translate the langauge to another language

Interpreters and compilers have a lot of similarities
- both involve a lexer and parser, that work together to create an AST
- it is when they traverse the AST that they diverge


## What the compiler produces
So we know the compiler creates something written in another language; but what about the details?
- how does the compiler generate this target language from the AST?
- what is the target language?
- is the output in text or binary format?
- is the output in a file, or in memory?
- what exactly does it generate?
- is the translation 1-to-1?
 - what if the target language doesn't have the same concepts as the source language?

This depends on a lot of thigngs
- the source language
- the architecture of the machine that executes the target language
- how the output will be used (executed directly by machine, or interpreted, or compiled again, etc.)
- how fast the executable or compiler needs to be
- how much memory the executable or running image can use...
