# Some terminology

NOTE:
- the Monkey language has prefix and inflix operators, but not postfix operators
 - just to keep the scope of the project manageable


## Prefix Operator
The operator comes "before" the operand it acts on
```
-5
++i
!my_value
```


## Postfix Operator
The operator comes "after" the operand it acts on
```
i++
```


## Inflix Operator
An inflix operator sits between two operands
- they appear in binary expressions
```
1 + 2
3 * 4
```


## Operator Precedence
This is an idea that determines the priority that operators have when they appear in an expression

You can think of there being an ordered list of operators
- if two or more operators appear in an expression:
 - you go down the ordered list of operators
 - the ones that come earlier in the list get to act on their operands first
