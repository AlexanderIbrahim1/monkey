# String, Array, and Hash

So far, the compiler only supports three data types: integers, booleans, and NULL
This chapter covers implementing the string, the array, and the hash

We can reuse `StringObject`, `ArrayObject`, and `HashObject` from the interpreter

## Strings
String literals, like intergers, don't change between compile time and run time
- so we can treat them as constant expressions, in the `constants` stack