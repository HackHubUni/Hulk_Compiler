from Hulk.Parser.Hulk_Parser import get_hulk_parser
from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer

lexer = get_hulk_lexer()
print("lexer listo")
parser = get_hulk_parser()
print("parser listo")

w="(let a = 4 in a) @ \"hola\";"

tokens=lexer(w)

parser(tokens)