# Expressions in Monkey

Everything except for let-statements and return-statements is an expression in Monkey
Here are some examples of the operators we will implement in Monkey

## Unary operators
```
-5
!true
```

## Binary operators
```
5 + 5
5 - 5
5 * 5
5 / 5
foo == bar
foo != bar
foo < bar
foo > bar
```

## Parentheses for grouping
```
5 * (5 + 5)
((5 + 5) * 5) + 5
```

## Parentheses for calling
```
add(2, 3)
add(add(3, 4), add(5, 6))
```

## Identiiers as expressions
```
foo * bar / foobar
add(foo, bar)
```

## Function literals as expressions
Monkey allows using the `let` statement to bind a function to a name
```
let add = fn(x, y) { return x + y; };
```

## If "statements" as expressions
Similar to Rust, Monkey has "if expressions"
```
let result = if (10 > 5) { true } else { false };
```
