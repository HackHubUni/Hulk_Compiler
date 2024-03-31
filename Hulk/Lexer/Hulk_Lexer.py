from Hulk.Lexer.Regex import Get_Hulk_Regex
import os
import dill
import time
from Hulk.Lexer.utils import HulkLexer
import sys



def __create_hulk_lexer__():
    regex, eof = Get_Hulk_Regex()
    return HulkLexer(regex, eof)


def get_hulk_lexer(file_name='lexer.pkl', delete_before=False):

    # aumentar el número de llamados para que se pueda guardar el lexer
    sys.setrecursionlimit(5000)

    start_time = time.time()  # Start the timer

    route = os.getcwd()
    route = os.path.join(route, 'resources')

    raise_str = "No se puede entregar un lexer None"

    # Check if the directory exists, if not create it
    if not os.path.exists(route):
        os.makedirs(route)
    try:
        if delete_before:
            raise f"Se mandó a eliminar el lexer anterior"

        with open(os.path.join(route, file_name), 'rb') as lexer_file:
            lexer = dill.load(lexer_file)

        end_time = time.time()  # Stop the timer
        print(f"Time taken: {end_time - start_time} seconds")  # Print the time taken

        assert lexer is not None, raise_str
        return lexer
    except:
        lexer = __create_hulk_lexer__()

        with open(os.path.join(route, file_name), 'wb') as lexer_file:
            dill.dump(lexer, lexer_file)

        end_time = time.time()  # Stop the timer
        print(f"Time taken: {end_time - start_time} seconds")  # Print the time taken

        assert lexer is not None, raise_str
        return lexer




"""
a=get_hulk_lexer()

s=a("kdks")
print(s)
"""