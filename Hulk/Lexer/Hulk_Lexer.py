from Hulk.Lexer.Regex import Get_Hulk_Regex
from Lexer_Parser.lexer import Lexer


def Get_Hulk_Lexer():
    regex, eof = Get_Hulk_Regex()
    return Lexer(regex, eof)




