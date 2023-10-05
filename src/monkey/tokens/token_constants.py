"""
Some of the Token instances always have the same TokenType and Literal pair. To decrease
the amount of boilerplate in the rest of the codebase, these Token instances are written
as constants here.
"""

import monkey.tokens.token_types as token_types
from monkey.tokens.monkey_token import Token

# special token types
EOF_TOKEN = Token(token_types.EOF, "")

# operators
ASSIGN_TOKEN = Token(token_types.ASSIGN, "=")
PLUS_TOKEN = Token(token_types.PLUS, "+")
MINUS_TOKEN = Token(token_types.MINUS, "-")
BANG_TOKEN = Token(token_types.BANG, "!")
ASTERISK_TOKEN = Token(token_types.ASTERISK, "*")
SLASH_TOKEN = Token(token_types.SLASH, "/")
LT_TOKEN = Token(token_types.LT, "<")
GT_TOKEN = Token(token_types.GT, ">")
EQ_TOKEN = Token(token_types.EQ, "==")
NOT_EQ_TOKEN = Token(token_types.NOT_EQ, "!=")

# punctuation
COMMA_TOKEN = Token(token_types.COMMA, ",")
SEMICOLON_TOKEN = Token(token_types.SEMICOLON, ";")

LPAREN_TOKEN = Token(token_types.LPAREN, "(")
RPAREN_TOKEN = Token(token_types.RPAREN, ")")
LBRACE_TOKEN = Token(token_types.LBRACE, "{")
RBRACE_TOKEN = Token(token_types.RBRACE, "}")

# reserved keywords
FUNCTION_TOKEN = Token(token_types.FUNCTION, "FUNCTION")
LET_TOKEN = Token(token_types.LET, "LET")
TRUE_TOKEN = Token(token_types.TRUE, "TRUE")
FALSE_TOKEN = Token(token_types.FALSE, "FALSE")
IF_TOKEN = Token(token_types.IF, "IF")
ELSE_TOKEN = Token(token_types.ELSE, "ELSE")
RETURN_TOKEN = Token(token_types.RETURN, "RETURN")


SINGLE_CHAR_TOKEN_DICT: dict[str, Token] = {
    "=": ASSIGN_TOKEN,
    "+": PLUS_TOKEN,
    "-": MINUS_TOKEN,
    "!": BANG_TOKEN,
    "*": ASTERISK_TOKEN,
    "/": SLASH_TOKEN,
    "<": LT_TOKEN,
    ">": GT_TOKEN,
    ",": COMMA_TOKEN,
    ";": SEMICOLON_TOKEN,
    "(": LPAREN_TOKEN,
    ")": RPAREN_TOKEN,
    "{": LBRACE_TOKEN,
    "}": RBRACE_TOKEN,
}
