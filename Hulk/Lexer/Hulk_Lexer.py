from Hulk.Lexer.Regex import Get_Hulk_Regex
from Lexer_Parser.lexer import Lexer
import os
import dill
from Lexer_Parser.lexer import Lexer

"""
def __hulk_lexer__():
    regex, eof = Get_Hulk_Regex()
    return Lexer(regex, eof)


def get_hulk_lexer(save_dir: str = 'save'):
    
    #Devuelve el lexer del Hulk
    
    # Definir la ruta del archivo serializado
    os.makedirs(save_dir, exist_ok=True)  # Crea la carpeta si no existe
    file_path = os.path.join(save_dir, 'lexer.pkl')
    lexer: Lexer = None

    # Verificar si el archivo serializado existe
    if os.path.exists(file_path):
        try:
            # Intentar cargar el objeto serializado
            with open(file_path, 'rb') as f:
                lexer = dill.load(f)
        except EOFError:
            # Si hay un error EOF, eliminar el archivo corrupto y crear un nuevo objeto
            os.remove(file_path)
            lexer = __hulk_lexer__()
            with open(file_path, 'wb') as f:
                dill.dump(lexer, f)
    else:
        # Si no existe, crear el objeto y serializarlo
        lexer = __hulk_lexer__()
        with open(file_path, 'wb') as f:
            dill.dump(lexer, f)

    if lexer is None:
        raise Exception("Error al cargar el lexer")
    return lexer


get_hulk_lexer()
"""
print("Ready Lexer")

def get_hulk_lexer():
    regex, eof = Get_Hulk_Regex()
    return Lexer(regex, eof)


