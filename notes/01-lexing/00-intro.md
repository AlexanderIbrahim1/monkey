# Lexical Analysis

It is difficult to interpret plain text in a programming language as another programming language
- we need to turn the source code into a more accessible form

The first step is *lexing*:
- this is the part where we turn the source code into tokens


## Tokens
Tokens are small, easily categorizable data structures
- they are easier and more featureful for a programming language to work with compared to plain text

What is the point of creating tokens?
- in a later step called "parsing", we take these tokens, and feed them into a parser (next chapter)

### Types of Tokens
Depending on the language, the lexer will categorize each part of the source code as a separate token
Some common categories:

+ reserved keywords
 - `if`, `else`, `for`, `let`, `int`, `float`, `char`, `struct`, `class`, etc.
+ identifiers
 - names given to variables, functions, classes
+ literals
 - each literal often gets its own type of token (i.e. one for integers, one for booleans, ...)
+ operators
 - operators like `+, -, *, /, ==` get their own tokens
+ punctuation
 - there are special characters for separating code elements: `(`, `)`, `{`, `}`, `[`, `.`, `::`, etc.
+ whitespace
 - in some languages, whitespace is important (like Python), and they get their own tokens
 - in Monkey, whitespace is ignored completely; its only purpose is to separate tokens
+ preprocessor directives
 - in C and C++, preprocessor directives like `#include` are treated as tokens
+ line number, column number, filename
 - this information is useful for debugging or error reporting to the user

Pretty much anything in the source code that could mean something, is treated as a token
- what matters depends on the language being interpreted

### Example:
The book gives the following example: `let x = 5 + 5;`
After passing it through the lexer, we might get something like this:
```
tokens = [
    LET,
    IDENTIFIER("x"),
    EQUALS_SIGN,
    INTEGER(5),
    PLUS_SIGN,
    INTEGER(5),
    SEMICOLON,
]
```
