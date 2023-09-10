"""
This module contains constants representing all the token types recognized by the
Monkey programming language.
"""

TokenType = str
Literal = str

# special token types
ILLEGAL = "ILLEGAL"
EOF = "EOF"

# identifiers
IDENTIFIER = "IDENTIFIER"

# literals
INT = "INT"

# operators
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
LT = "<"
GT = ">"
EQ = "=="
NOT_EQ = "!="

# punctuation
COMMA = ","
SEMICOLON = ";"

LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"

# reserved keywords
FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
RETURN = "RETURN"
