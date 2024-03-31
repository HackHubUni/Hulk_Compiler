from Hulk.Parser.Hulk_Parser import get_hulk_parser
from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer

def test0():
    print("Test 0")
    ast=get_ast('-5;')
    print("Finish test 0")

test0()
