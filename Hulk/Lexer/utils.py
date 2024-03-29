from cmp.pycompiler import Token, Terminal,Grammar
from Lexer_Parser.lexer import Lexer
import os
import dill


class SerializeLexer(Lexer):
    def __init__(self, table: [(Terminal, str)], eof):
        save_dir = "save"
        os.makedirs(save_dir, exist_ok=True)  # Crea la carpeta si no existe

        # Definir las rutas de los archivos serializados
        eof_file_path = os.path.join(save_dir, 'eof.pkl')
        regexs_file_path = os.path.join(save_dir, 'regexs.pkl')
        automaton_file_path = os.path.join(save_dir, 'automaton.pkl')

        # Intentar cargar los objetos serializados
        try:
            with open(eof_file_path, 'rb') as f:
                self.eof = dill.load(f)
            with open(regexs_file_path, 'rb') as f:
                self.regexs = dill.load(f)
            with open(automaton_file_path, 'rb') as f:
                self.automaton = dill.load(f)
        except (EOFError, FileNotFoundError):
            # Si hay un error EOF o los archivos no existen, crear un nuevo Lexer
            super().__init__(table, eof)

            # Serializar los atributos
            with open(eof_file_path, 'wb') as f:
                dill.dump(self.eof, f)
            with open(regexs_file_path, 'wb') as f:
                dill.dump(self.regexs, f)
            with open(automaton_file_path, 'wb') as f:
                dill.dump(self.automaton, f)
