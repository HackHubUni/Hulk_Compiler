import enum

from Hulk.Interpreter.interpreter_errors import InterpreterError
from Hulk.Semantic_Check.basic_types.semantic_errors import SemanticError

def parse_string(s):
    # Intentar convertir a booleano
    if s.lower() == 'true' or s.lower() == 'false':
        return 'bool'
    # Intentar convertir a float
    try:
        float(s)
        return 'float'
    except ValueError:
        pass
    # Si no se puede convertir a booleano o float, es un string
    return 'str'
class Dynamic_Types():
     #tags = ['Number', 'String', 'Boolean', 'None', 'Unknown']
    def __init__(self,tags:list[str]):
        self.tags:list[str]=tags
     # Crear el enum dinámicamente con el nuevo tag
        self.DynamicEnum = enum.Enum('DynamicType_Enum', tags)

    def get_tag(self,type_name:str):
        """Retorna el tag correspondiente al type"""
        try:
            tag = getattr(self.DynamicEnum, type_name)
            return tag
        except AttributeError:
            raise SemanticError(f"El type {type_name} no existe")

    def __str__(self):
    # Imprimir los miembros del enum
        for tag in self.DynamicEnum:
            print(tag)


class TypeContainer:
    def __init__(self,value,type:Dynamic_Types):
        self.value = value
        self.type:Dynamic_Types = type



    def __str__(self):
        return str(self.value)

