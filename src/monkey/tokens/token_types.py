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
STRING = "STRING"

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
COLON = ":"
COMMA = ","
SEMICOLON = ";"

LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
LBRACKET = "["
RBRACKET = "]"

# reserved keywords
FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
RETURN = "RETURN"
