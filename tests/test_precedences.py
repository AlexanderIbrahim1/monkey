from monkey.parser.precedences import Precedence


def test_precedence_comparison():
    p_lowest = Precedence.LOWEST
    p_equals = Precedence.EQUALS

    assert p_lowest < p_equals
