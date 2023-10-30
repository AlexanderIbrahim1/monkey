# Chapter 04 - Compiling Conditionals

We need to get the VM to execute different bytecode depending on a condition
- in the interpreter, this was easy
 - we had an `IfExpression` object that held the condition, consequence, and alternative
 - a simple if-statement in the evaluation was all we needed
 - it was because of this nested structure, which allowed us to easily pick one or the other,
   that we could do this so simply

In the compiler, this is much more difficult
- the condition, consequence, and alternative are all turned into bytecode instructions
 - they are stored, one-after-the-other, inside the sequence of instructions
 - suppose they are stored like "condition -- consequence -- alternative"
  1. suppose we must run the consequence; how can we stop and skip the alternative?
  2. suppose we must run the alternative; how can we skip over the consequence?
  - by even iterating over the bytecode, the VM will run them both!

We solve this using jump instructions!