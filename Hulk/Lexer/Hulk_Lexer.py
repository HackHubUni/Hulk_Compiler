from Hulk.Lexer.Regex import Get_Hulk_Regex
from Lexer_Parser.lexer import Lexer


def get_hulk_lexer():
    regex, eof = Get_Hulk_Regex()
    return Lexer(regex, eof)





