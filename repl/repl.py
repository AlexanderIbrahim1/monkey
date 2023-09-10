"""
This module contains our REPL for the Monkey language.
"""

from monkey import Lexer
from monkey import token_types

EMPTY_INPUTS = ["", "\n", "\r\n"]


def main() -> None:
    print("Hello! This is the Monkey programming langauge!")
    print("Feel free to type in commands!")

    while True:
        user_input = input("\n>> ")

        if user_input in EMPTY_INPUTS:
            break

        lexer = Lexer(user_input)

        token = lexer.next_token()
        while token.token_type != token_types.EOF:
            print(token)
            token = lexer.next_token()

    print("Goodbye!")


if __name__ == "__main__":
    main()
