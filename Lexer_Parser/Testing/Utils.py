from Lexer_Parser.parser.shift_reduce import evaluate_reverse_parse
from cmp.ast import BinaryNode, ConstantNumberNode, get_printer
def parse(text: str):
    """
    Parsea la cadena, printea los token las producciones y las operaciones shift reduce adeams del ast
    :param text:
    :return:
    """
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
    print(f" \n El ast es: \n {printer(ast)}")