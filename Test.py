from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer
from Hulk.Parser.Hulk_Parser import get_hulk_parser
from Hulk.Semantic_Check.check_type_semantic import InfoSaverTree,TypeBuilder
from cmp.evaluation import evaluate_reverse_parse
from Hulk.Semantic_Check.type_inferator import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.type_inferator import *
from Hulk.Semantic_Check.checker import *
from Hulk.Semantic_Check.type_node import *

# import lexer and parser
lexer = get_hulk_lexer()
parser = get_hulk_parser()

print("Lexer and parser Ok")


import os

# Ruta a la carpeta 'Examples' que es subcarpeta de 'Hulk'
path = 'Hulk/Examples'

# Array para almacenar los nombres de las carpetas
folders=["Expressions","Functions","Variables","Conditionals","Loops","Types","Type_checking","Type_inference","Protocols","Iterables","Vectors"]

def print_line_separator(length:int):
    print('='*length)

def get_subfolder(path:str):
        # Recorrer los archivos y carpetas en 'path'
        folders=[]
        for name in os.listdir(path):
            # Comprobar si es una carpeta
            if os.path.isdir(os.path.join(path, name)):
                folders.append(name)

        return folders

def get_folder(folders:list[str]):
        """
        Devuelve la carpeta a necesitar
        """
        # Recorrer las carpetas en 'folders'
        for folder in folders:
                yield folder
def get_file_examples(folder:str):
        global path
        # Variable para almacenar el contenido de los archivos .hulk
        text = ''
        # Recorrer los archivos en la carpeta
        for filename in os.listdir(os.path.join(path, folder)):
            # Comprobar si el archivo tiene la extensión .hulk
            if filename.endswith('.hulk'):
                # Abrir el archivo y añadir su contenido a 'text'
                with open(os.path.join(path, folder, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    yield text



def evaluate(text:str,is_printting:bool=True):


        tokens = lexer(text)


        if is_printting:
            print(f"Los tokens son: \n {tokens}")
        #Parsear
        parse, operations = parser(tokens)

       # print(len(parse),"parser")
       # print(len(operations),"operation")
       # print(len(tokens),"len tokens")


        ast = evaluate_reverse_parse(parse, operations, tokens)

        errors = []
        collector = InfoSaverTree(errors)
        collector.visit(ast)
        if is_printting:
            print(f"El ast es \n {ast}")
        context = collector.context

        builder = TypeBuilder(context, errors)
        assert len(errors)==0, "No puede tener errores de semántica"
        builder.visit(ast)
        if is_printting:
            print('Errors:', errors)
            print("contexto \n ", 'Context:')
            print(context)
        checker = TypeChecker(context, errors)
        if is_printting:
            print(checker)
        scope = checker.visit(ast)
        if is_printting:
            print(scope)


#def test():
#        global folders
#        for folder in folders:
#                for file in get_file_examples(folder):
#                        evaluate(file)



def show():
    global folders
    for folder in folders:
        for file in get_file_examples(folder):
            print(f' Se va a parsear \n {file } \n respuesta: \n ')
            evaluate(file)


def show_errors():
    global folders
    for folder in folders:
        for file in get_file_examples(folder):

            try:
                #print(f' Se va a parsear \n {file} \n respuesta: \n ')
                evaluate(file,is_printting=False)
            except Exception as e:
                print_line_separator(20)
                print("Error en el archivo", file)
                print("Detalle del error:", str(e))
                print_line_separator(50)

if __name__=="__main__":
    show_errors()