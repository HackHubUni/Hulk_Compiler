from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer
from Hulk.Parser.Hulk_Parser import get_hulk_parser
from Hulk.Semantic_Check.check_semantics import check_semantics
from Hulk.Semantic_Check.basic_types.scopes import *

# from Hulk.Semantic_Check.check_type_semantic import CheckTypes,TypeBuilder
from cmp.evaluation import evaluate_reverse_parse


# import lexer and parser
lexer = get_hulk_lexer()
parser = get_hulk_parser()

print("Lexer and parser Ok")


def evaluate(text: str):

    tokens = lexer(text)

    print(f"Los tokens son: \n {tokens}")
    # Parsear
    print("\nComenzando a Parsear:\n")
    parse, operations = parser(tokens)

    ast = evaluate_reverse_parse(parse, operations, tokens)
    print(f"El ast es \n {str(ast)}")
    # Check Semantics
    print("\nComenzando a Chequear la Semántica:\n")
    errors = []
    scope = HulkScopeLinkedNode()

    if not check_semantics(ast, scope, errors):
        print("Errores de semántica:")
        for error in errors:
            print(f" - {error}")
        return
    else:
        print("No hay errores de semántica")


with open("./examples/tricky_inference.hulk", "r") as file:
    text: str = file.read()
    evaluate(text)
