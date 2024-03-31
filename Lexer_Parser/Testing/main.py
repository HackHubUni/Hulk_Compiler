from cmp.pycompiler import Grammar
from Lexer_Parser.parser.shift_reduce import LR1Parser, evaluate_reverse_parse
from Lexer_Parser.Lexer.lexer import Lexer
from cmp.ast import BinaryNode, ConstantNumberNode, PlusNode, \
    EqualNode, get_printer

G = Grammar()  # Crear gramatica
E = G.NonTerminal('E', True)
A = G.NonTerminal('A')
equal, plus, num = G.Terminals('= + int')

######################
# Producciones de la gramatica
################

E %= num, lambda h, s: ConstantNumberNode(s[1]), None
E %= A + equal + A, lambda h, s: EqualNode(s[1], s[3]), None, None, None
A %= num + plus + A, lambda h, s: PlusNode(ConstantNumberNode(s[1]), s[3]), None, None, None
A %= num, lambda h, s: ConstantNumberNode(s[1]), None

# parser
parser = LR1Parser(G)

# Lexer

lexer = Lexer(
    [
        (num, '(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'),

        ('space', '( |\t|\n)( |\t|\n)*'),

        (equal, '='),
        (plus, '\+'),

    ], G.EOF
)
text = "1+2=3"
text = "6+7=13"
all_tokens = lexer(text)
tokens = list(filter(lambda token: token.token_type != 'space', all_tokens))
print(f"Los tokens son {tokens}")
right_parse, operations = parser(tokens)
print(right_parse)
print("-----------------------------")
print(operations)
print("###############################")

ast = evaluate_reverse_parse(right_parse, operations, tokens)

printer = get_printer(AtomicNode=ConstantNumberNode, BinaryNode=BinaryNode)
print(f"El ast es: \n {printer(ast)}")
