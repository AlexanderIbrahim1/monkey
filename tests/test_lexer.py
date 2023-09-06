import pytest


from monkey import Lexer
from monkey import Token
from monkey import Token
from monkey import token_types


class TestLexer:
    def test_basic(self):
        input_text = r"=;(){},+"
        lexer = Lexer(input_text)

        assert lexer.next_token() == Token(token_types.ASSIGN, '=')
        assert lexer.next_token() == Token(token_types.SEMICOLON, ';')
        assert lexer.next_token() == Token(token_types.LPAREN, '(')
        assert lexer.next_token() == Token(token_types.RPAREN, ')')
        assert lexer.next_token() == Token(token_types.LBRACE, '{')
        assert lexer.next_token() == Token(token_types.RBRACE, '}')
        assert lexer.next_token() == Token(token_types.COMMA, ',')
        assert lexer.next_token() == Token(token_types.PLUS, '+')
        assert lexer.next_token() == Token(token_types.EOF, '' )

    def test_raises_invalid_char(self):
        input_text = r"~"
        lexer = Lexer(input_text)
        with pytest.raises(ValueError):
            lexer.next_token()
