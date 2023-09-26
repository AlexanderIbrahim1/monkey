# 3.3 - A Tree-walking Interpreter

Our Monkey language interpreter will be a tree-walking interpreter
- the AST will be executed on-the-fly with no IR or compilation step
- there won't be an executable artifact created by this (that's for the next book)

This interpreter is heavily inspired by "The Structure and Interpretation of Computer Programs (SICP)"
- it is an easy way to get started, understand what is going on, and extend later on

We need two things for evaluation:
1. a way to represent the values that get evaluated
2. a recursive, tree-walking evaluator

The evaluator is literally just one function called `eval`
Some of its properties:
- it is recursive (when it finds an infix expression, it evaluates the left and right sides)
- it works on the "values" that we want to represent


## Representing Objects
We need a way to represent the values that we generate when we evaluate the AST

For example, suppose we have the following code:
```
let a = 5;
a + a;
```
- we need to access the value that `a` is bound to; we need to get the `5`
- the AST represents it using an `IntegerLiteral` expression
 - but we need a way to keep track of this IntegerLiteral while evaluating the rest of the AST!


What are our options?
- some interpreters use native types of the host langauge to represent these values
- some interpreters use wrappers around the native types of the host langauge
- the choices depend on the host language capabilities, and the target language requirements

An important influence on the design is performance
- suppose we want a fast interpreter that doesn't take up too much memory:
 - we need a fast host language and a lean value system
- if performance doesn't matter as much, we can go simpler


## The Monkey Language Evlauation System
The book chooses to represent each value in the monkey source code as an "Object"
- this is just a struct that wraps the value
