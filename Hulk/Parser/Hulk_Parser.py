import os
import dill
from Lexer_Parser.shift_reduce import LR1Parser
from Hulk.Grammar.gramarlr1 import Gramarlr1


def get_hulk_parser(save_dir: str = 'save'):
    """
    Devuelve el parser del Hulk
    """
    # Definir la ruta del archivo serializado

    os.makedirs(save_dir, exist_ok=True)  # Crea la carpeta si no existe
    file_path = os.path.join(save_dir, 'parser.pkl')
    parser: LR1Parser = None

    # Verificar si el archivo serializado existe
    if os.path.exists(file_path):
        try:
            # Intentar cargar el objeto serializado
            with open(file_path, 'rb') as f:
                parser = dill.load(f)
        except EOFError:
            # Si hay un error EOF, eliminar el archivo corrupto y crear un nuevo objeto
            os.remove(file_path)

            Grammar = Gramarlr1().Grammar
            parser = LR1Parser(Grammar)
            with open(file_path, 'wb') as f:
                dill.dump(parser, f)
    else:
        # Si no existe, crear el objeto y serializarlo
        Grammar = Gramarlr1().Grammar
        parser = LR1Parser(Grammar)
        with open(file_path, 'wb') as f:
            dill.dump(parser, f)

    if parser is None:
        raise Exception("Error al cargar el parser")
    return parser


print("Ready Parser")