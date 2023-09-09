import pytest


from monkey import Lexer
from monkey import Token
from monkey import token_types


class TestLexer:
    def test_basic(self):
        input_text = r"=;(){},+"
        lexer = Lexer(input_text)

        assert lexer.next_token() == Token(token_types.ASSIGN, "=")
        assert lexer.next_token() == Token(token_types.SEMICOLON, ";")
        assert lexer.next_token() == Token(token_types.LPAREN, "(")
        assert lexer.next_token() == Token(token_types.RPAREN, ")")
        assert lexer.next_token() == Token(token_types.LBRACE, "{")
        assert lexer.next_token() == Token(token_types.RBRACE, "}")
        assert lexer.next_token() == Token(token_types.COMMA, ",")
        assert lexer.next_token() == Token(token_types.PLUS, "+")
        assert lexer.next_token() == Token(token_types.EOF, "")

    @pytest.mark.skip
    def test_sample_monkey_code(self):
        monkey_code = "\n".join(
            [
                "let five = 5;               ",
                "let ten = 10;               ",
                "                            ",
                "let add = fn(x, y) {        ",
                "   x + y;                   ",
                "};                          ",
                "                            ",
                "let result = add(five, ten);",
            ]
        )

        lexer = Lexer(monkey_code)

        expected = [
            Token(token_types.LET, "let"),
            Token(token_types.IDENTIFIER, "five"),
            Token(token_types.ASSIGN, "="),
            Token(token_types.INT, "5"),
            Token(token_types.SEMICOLON, ";"),
            Token(token_types.LET, "let"),
            Token(token_types.IDENTIFIER, "ten"),
            Token(token_types.ASSIGN, "="),
            Token(token_types.INT, "10"),
            Token(token_types.SEMICOLON, ";"),
            Token(token_types.LET, "let"),
            Token(token_types.IDENTIFIER, "add"),
            Token(token_types.ASSIGN, "="),
            Token(token_types.FUNCTION, "fn"),
            Token(token_types.LPAREN, "("),
            Token(token_types.IDENTIFIER, "x"),
            Token(token_types.COMMA, ","),
            Token(token_types.IDENTIFIER, "y"),
            Token(token_types.RPAREN, ")"),
            Token(token_types.LBRACE, "{"),
            Token(token_types.IDENTIFIER, "x"),
            Token(token_types.PLUS, "+"),
            Token(token_types.IDENTIFIER, "y"),
            Token(token_types.SEMICOLON, ";"),
            Token(token_types.RBRACE, "}"),
            Token(token_types.SEMICOLON, ";"),
            Token(token_types.LET, "let"),
            Token(token_types.IDENTIFIER, "result"),
            Token(token_types.ASSIGN, "="),
            Token(token_types.IDENTIFIER, "add"),
            Token(token_types.LPAREN, "("),
            Token(token_types.IDENTIFIER, "five"),
            Token(token_types.COMMA, ","),
            Token(token_types.IDENTIFIER, "ten"),
            Token(token_types.RPAREN, ")"),
            Token(token_types.SEMICOLON, ";"),
            Token(token_types.EOF, ""),
        ]

        actual = [lexer.next_token() for _ in range(len(expected))]

        assert expected == actual

    def test_illegal(self):
        input_text = r"~"
        lexer = Lexer(input_text)
        assert lexer.next_token().token_type == token_types.ILLEGAL

    def test_read_identifier(self):
        lexer = Lexer(r"hello")
        assert lexer.next_token() == Token(token_types.IDENTIFIER, "hello")

    @pytest.mark.parametrize(
        "keyword, token",
        [
            ("let", Token(token_types.LET, "let")),
            ("fn", Token(token_types.FUNCTION, "fn")),
        ]
    )
    def test_read_keyword(self, keyword: str, token: Token):
        lexer = Lexer(keyword)
        assert lexer.next_token() == token

    def test_read_with_whitespace(self):
        lexer = Lexer("let x = y;")

        expected = [
            Token(token_types.LET, "let"),
            Token(token_types.IDENTIFIER, "x"),
            Token(token_types.ASSIGN, "="),
            Token(token_types.IDENTIFIER, "y"),
            Token(token_types.SEMICOLON, ";"),
        ]

        actual = [lexer.next_token() for _ in range(len(expected))]

        assert expected == actual
