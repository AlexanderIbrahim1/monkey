import pytest


from monkey import Lexer
from monkey import Token
from monkey import token_types


class TestLexer:
    def test_basic(self):
        input_text = r"=;(){},+-!*/<>"
        lexer = Lexer(input_text)

        assert lexer.next_token() == Token(token_types.ASSIGN, "=")
        assert lexer.next_token() == Token(token_types.SEMICOLON, ";")
        assert lexer.next_token() == Token(token_types.LPAREN, "(")
        assert lexer.next_token() == Token(token_types.RPAREN, ")")
        assert lexer.next_token() == Token(token_types.LBRACE, "{")
        assert lexer.next_token() == Token(token_types.RBRACE, "}")
        assert lexer.next_token() == Token(token_types.COMMA, ",")
        assert lexer.next_token() == Token(token_types.PLUS, "+")
        assert lexer.next_token() == Token(token_types.MINUS, "-")
        assert lexer.next_token() == Token(token_types.BANG, "!")
        assert lexer.next_token() == Token(token_types.ASTERISK, "*")
        assert lexer.next_token() == Token(token_types.SLASH, "/")
        assert lexer.next_token() == Token(token_types.LT, "<")
        assert lexer.next_token() == Token(token_types.GT, ">")
        assert lexer.next_token() == Token(token_types.EOF, "")

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
            ("true", Token(token_types.TRUE, "true")),
            ("false", Token(token_types.FALSE, "false")),
            ("if", Token(token_types.IF, "if")),
            ("else", Token(token_types.ELSE, "else")),
            ("return", Token(token_types.RETURN, "return")),
        ],
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

    @pytest.mark.parametrize(
        "integer, token",
        [
            (3, Token(token_types.INT, "3")),
            (5, Token(token_types.INT, "5")),
            (20, Token(token_types.INT, "20")),
        ],
    )
    def test_read_positive_integer(self, integer, token):
        lexer = Lexer(f"{integer}")
        assert lexer.next_token() == token

    @pytest.mark.parametrize(
        "operator, token",
        [
            ("!=", Token(token_types.NOT_EQ, "!=")),
            ("==", Token(token_types.EQ, "==")),
        ],
    )
    def test_twochar_operators(self, operator, token):
        lexer = Lexer(f"{operator}")
        assert lexer.next_token() == token

    def test_assign_only(self):
        lexer = Lexer("=")
        assert lexer.next_token() == Token(token_types.ASSIGN, "=")

    def test_failed_lexer_empty(self):
        lexer = Lexer("")
        assert lexer.has_errors()

    @pytest.mark.parametrize("monkey_text", ["hello", "hello    ", "hello; world  "])
    def test_failed_lexer_no_semicolon_end(self, monkey_text):
        lexer = Lexer(monkey_text)
        assert lexer.has_errors()
