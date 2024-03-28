import os
import dill
from Lexer_Parser.shift_reduce import LR1Parser
from Hulk.Grammar.gramarlr1 import Gramarlr1

# Definir la ruta del archivo serializado
save_dir = 'save'
os.makedirs(save_dir, exist_ok=True)  # Crea la carpeta si no existe
file_path = os.path.join(save_dir, 'parser.pkl')

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
print("Ready Parser")