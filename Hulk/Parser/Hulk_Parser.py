import os
import dill
import time
import sys
from Hulk.Parser.utils import Hulk_Parser_Container
from Hulk.Grammar.gramarlr1 import Gramarlr1


def __create_hulk_parser__():
    Grammar = Gramarlr1().Grammar
    print("Crear el Parser")
    parser = Hulk_Parser_Container(Grammar)
    print("Parser Creado")
    return parser




def get_hulk_parser(file_name='parser.pkl', delete_before=False):

    # aumentar el número de llamados para que se pueda guardar el lexer
    sys.setrecursionlimit(5000)

    start_time = time.time()  # Start the timer

    route = os.getcwd()
    route = os.path.join(route, 'resources')

    # Check if the directory exists, if not create it
    if not os.path.exists(route):
        os.makedirs(route)
    try:
        if delete_before:
            raise "Se mandó a eliminar el parser anterior"

        with open(os.path.join(route, file_name), 'rb') as parser_file:
            parser = dill.load(parser_file)

        end_time = time.time()  # Stop the timer
        print(f"Time taken: {end_time - start_time} seconds")  # Print the time taken

        assert parser is not None, "No se puede entregar un parser None"
        return parser
    except:
        parser = __create_hulk_parser__()

        with open(os.path.join(route, file_name), 'wb') as parser_file:
            dill.dump(parser, parser_file)

        end_time = time.time()  # Stop the timer
        print(f"Time taken: {end_time - start_time} seconds")  # Print the time taken

        assert parser is not None, "No se puede entregar un parser None"
        return parser

print("Ready the Parser")
