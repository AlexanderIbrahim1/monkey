# Pratt Parser

TODO:
- go back and expand on these notes once I've implemented parts of the Pratt Parser to get a feeling for
  how it actually works






The Pratt Parser is a top-down recursive-descent parser
- it is well-suited for parsing expressions with operators of different precedence levels and associativity
- it does this using a technique called "precedence climbing"

The main ideas behind the Pratt Parser?
- we associate "parsing functions" with "token types"

NOTE:
- not every token gets a parsing function


## Operator Table
The Pratt parser holds a table of operators
- each operator has a precedence level (value) and an associativity (left-associative or right-associative)


## Recursiveness
The parser processes the tokens one-by-one in a recursive manner

Suppose it is parsing tokens left-to-right, and holds a certain precedence level
1. it then encounters a new token that represents an operator
 - it looks up the precedence of this new operator
2. if the new operator's precedence is greater than the current precedence level:
  - it recursively parses the subexpression to the right
 - else:
  - it recursively parses the subexpression to the left
3. it repeats this process until the entire expression is parsed


