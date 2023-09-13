# 2.6 - Parsing Expressions

Parsing statements is straightforward:
- we process tokens from left to right
- we expect or reject the current and peeked-at tokens
- if everything works out, we return an AST node

Parsing expressions is much more complicated


## Operator precedence
Suppose we have an arithmetic expression: `5 * 5 + 10`
- this is equivalent to `( (5 * 5) + 10 )`

However, we might have an expression like `5 * (5 + 10)`
- the precedence of `()` is higher than that of `*`, which is higher than that of `+`

Our parser must take details like this into account


## Repeated tokens appearing
Let's look at some statements:
1. a let-statement looks like: `let <identifier> = <expression>;`
 - there is one `let`, one identifier, one assignment, one semicolon
2. a return-statement looks like: `return <expression>;`
 - there is one `return` and one semicolon

Because the tokens are unique (aside from whatever is inside an expression), statements are easier to parse

However, an expression can have multiple tokens of the same type
- for example: `-5 - 10`
 - there are two `-` tokens, and two `int` tokens


## The same token representing different things
Consider the following expression: `5 * (add(2, 3) + 10)`
- the inner pair `()` denotes a call expression
- the outer pair `()` denotes a grouping

The validity of a token's position now depends on the context!
