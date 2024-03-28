from Lexer_Parser.shift_reduce import LR1Parser, evaluate_reverse_parse
from Hulk.Grammar.gramarlr1 import Gramarlr1

Grammar = Gramarlr1().Grammar

parser = LR1Parser(Grammar)

print("Ok")