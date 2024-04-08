import enum

from Hulk.Interpreter.interpreter_errors import InterpreterError
from Hulk.Semantic_Check.basic_types.semantic_errors import SemanticError


def is_same_as_tag(name: str, tag: 'DynamicType_Enum'):
    """
    Devuelve si el nombre que se pasa como string es el mismo
     que el que tiene el tag del Enum (tag)
    """
    return name == tag.name


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
    # tags = ['Number', 'String', 'Boolean', 'None', 'Unknown']
    def __init__(self, tags: list[str]):
        self.tags: list[str] = tags
        # Crear el enum dinámicamente con el nuevo tag
        self.DynamicEnum = enum.Enum('DynamicType_Enum', tags)

    def get_tag(self, type_name: str):
        """Retorna el tag correspondiente al type"""
        try:
            tag = getattr(self.DynamicEnum, type_name)
            return tag
        except AttributeError:
            raise SemanticError(f"El type {type_name} no existe")

            # ...

    # def is_same_as_tag(self, s: str):
    #     """Verifica si el string dado es igual al nombre de uno de los tags"""
    #     return s in self.DynamicEnum.__members__

    def __str__(self):
        # Imprimir los miembros del enum
        for tag in self.DynamicEnum:
            print(tag)


class TypeContainer:

    def check(self):
        # if "<None>" == self.type.name:
        if is_same_as_tag("<None>", self.type):
            raise SemanticError("No se permiten tipos de None")

    def __init__(self, value, type: Dynamic_Types):
        self.value = value
        self.type: Dynamic_Types = type
        self.check()

    def __str__(self):
        return str(self.value)


class NullTypeContainer(TypeContainer):

    def check(self):
        if not is_same_as_tag("<None>", self.type):
            raise SemanticError("No es de type <None>")

    def __init__(self, value, type: Dynamic_Types):
        super().__init__(value, type)


class UnknownTypeContainer(TypeContainer):
    def check(self):
        if not is_same_as_tag("Unknown", self.type):
            raise SemanticError("No es de type Unknown")

    def __init__(self, value, type: Dynamic_Types):
        super().__init__(value, type)
