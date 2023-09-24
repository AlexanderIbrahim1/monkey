"""
This module contains our REPL for the Monkey language.
"""

from monkey import Lexer
from monkey import Parser

EMPTY_INPUTS = ["", "\n", "\r\n"]


def main() -> None:
    print("Hello! This is the Monkey programming langauge!")
    print("Feel free to type in commands!")

    while True:
        user_input = input("\n>> ")

        if user_input in EMPTY_INPUTS:
            break

        lexer = Lexer(user_input)
        parser = Parser(lexer)
        program = parser.parse_program()

        if parser.has_errors():
            print("PARSING ERROR")
            print(parser.errors())
            continue

        for statement in program:
            print(statement)

    print("Goodbye!")


if __name__ == "__main__":
    main()
