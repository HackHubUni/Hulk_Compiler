from Hulk.Lexer.Regex import Get_Hulk_Regex
from Lexer_Parser.lexer import Lexer
import os
import dill
from Lexer_Parser.lexer import Lexer
from cmp.pycompiler import Grammar
from Hulk.Lexer.utils import SerializeLexer



def get_hulk_lexer():
    regex, eof = Get_Hulk_Regex()
    return SerializeLexer(regex, eof)





