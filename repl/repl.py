"""
This module contains our REPL for the Monkey language.
"""

from monkey import Lexer
from monkey import Parser
from monkey import evaluate
import monkey.object as objs

EMPTY_INPUTS = ["", "\n", "\r\n"]


def main() -> None:
    print("Hello! This is the Monkey programming langauge!")
    print("Feel free to type in commands!")

    env = objs.Environment()
    while True:
        user_input = input("\n>> ")

        if user_input in EMPTY_INPUTS:
            break

        lexer = Lexer(user_input)
        parser = Parser(lexer)
        program = parser.parse_program()

        if program.has_errors():
            print("PARSING ERROR")
            print(program.errors())
            continue

        evaluated = evaluate(program, env)
        if evaluated != objs.NULL_OBJ:
            print(f"{evaluated}")

    print("Goodbye!")


if __name__ == "__main__":
    main()
