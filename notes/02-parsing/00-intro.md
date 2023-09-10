# Parsing

What is a parser?
- a software component that *takes input data* and returns *a data structure that represents the input*

For example, in javascript, `JSON.parse`:
- takes a string representing JSON as input
- returns a javascript "object" of key-value pairs

In most interpreters and compilers, the data structure is called an "abstract syntax tree" (AST)
- "abstract": because certain details in the source code are abstracted away
- "syntax tree": the AST is commonly represented using a tree of nodes (each node is a "syntactic construct")

While most ASTs are similar in concept, they differ greatly in implementations
- the implementation depends on the programming language being used


## Syntactic Analysis
While the parser builds up the AST, it analyzes the input, making sure it conforms to the expected structure
- this part of parsing is called "syntactic analysis"
- if some part of the source code doesn't make sense, we'll find out here


## Parser Generators
A parser generator is a tool that:
- takes the formal description of a language (in some data format)
- produces a parser for that language

Parsing is one of the most well-understood branches of CS
- a lot of knowledge and effort have gone into creating these parser generators

The Monkey language is a pedagogical tool, and one of its purposes is to explain how parsers work
- so we'll be building our own parser instead of using a pre-built parser generator


## Parsing Strategies
There are two main strategies when parsing a programming language:
1. top-down parsing
 - start with the root node of the AST, then descend
2. bottom-up parsing
 - start with all the branches of the AST, then build up to the root node

Both "top-down parsing" and "bottom-up parsing" have different variations
- for example, there are "recursive descent", "early", and "predictive" variants for top-down parsing

The Monkey language will use a "Pratt parser"
- this is a "recursive-descent operator-precedence" parser
- this is one of the conceptually simpler ways to approach parsers

As an example, Clang uses a recursive descent parser for C and C++


## Trade-offs
Because our parser is more of a pedagogical tool, it won't have all the bells and whistles lots of other have
- no formal proof of correctness
- rudimentary error-recovery process + detection of erroneous syntax
