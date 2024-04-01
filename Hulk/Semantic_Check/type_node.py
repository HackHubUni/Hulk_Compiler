from cmp.semantic import *
from Hulk.tools.Ast import *
from abc import ABC
from Hulk.tools.Ast import *


class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, "Object")


class NoneType(Type):
    def __init__(self):
        Type.__init__(self, "None")


class NumType(ObjectType):
    def __init__(self):
        Type.__init__(self, "Number")

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, NumType)


class StringType(ObjectType):
    def __init__(self):
        Type.__init__(self, "String")

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, StringType)


class BoolType(ObjectType):
    def __init__(self):
        Type.__init__(self, "Bool")

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, BoolType)


class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, "<error>")

    def conforms_to(self, other: Type):
        return True

    def bypass(self):
        return True

    def __eq__(self, other: Type):
        return isinstance(other, Type)


class Function:
    def __init__(self, name, function_pointer: FunctionDeclarationNode):
        self.name = name
        self.param_names = function_pointer.args
        self.return_type = function_pointer.return_type
        self.function_point:FunctionDeclarationNode = function_pointer

    def __str__(self):
        output = f"func {self.name}"
        output += " ("
        params = ", ".join(f"{n.id}:{n.type.name}" for n in self.param_names)
        output += params
        output += ") :"
        output += self.return_type.name
        return output

    def __eq__(self, other: Type):
        return (
            other.name == self.name and other.return_type == self.return_type
        )  # and \
        # other.param_types == self.param_types


class Protocol:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent: HulkScope = parent
        self.methods = []

    def define_method(
        self, name: str, param_names: list, param_types: list, return_type
    ):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def get_method(self, name: str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def __str__(self):
        output = f"protocol {self.name}"
        parent = (
            "" if self.parent is None else " : ".join(parent for parent in self.parent)
        )
        output += ": " + parent
        output += " {"
        output += "\n\t".join(str(x) for x in self.methods)
        output += "\n" if self.methods else ""
        output += "}\n"
        return output


class HulkScopeBase:
    def __init__(self) -> None:
        self.locals: dict[str:VariableInfo] = {}  # TODO
        self.children = []
        self.types: dict[str, Type] = {}
        self.function: dict[str, Function] = {}


class HulkScope(HulkScopeBase):
    def __init__(self, parent: HulkScopeBase):
        super().__init__()
        self.parent: HulkScope = parent

    # let x = 4 in                   // A = Scope {x = 5} parent = ScopeGlobal
    #      let y = 10 in             // Scope {y = 10}  parent = A
    #          while (x < y){
    #            x := x + 1          //
    #   }
    #

    def create_variable(self, variable_name: str, value_type: str) -> VariableInfo:
        """Create a new variable in the actual scope"""
        if variable_name in self.locals:
            raise SemanticError(f"The variable: {variable_name} is already defined")
        info = VariableInfo(variable_name, value_type)
        self.locals[variable_name] = info
        return info

    def find_variable(self, variable_name: str) -> VariableInfo:
        """Try to find the variable in the local scope and if it is not in here
        it tries to find it in the parent scope.
        And if the variable is not in any of the parent scopes it raise a semantic error
        """
        if variable_name in self.locals:
            return self.locals[variable_name]
        if not self.parent:
            raise SemanticError(f"The variable ({variable_name}) is not defined")
        return self.parent.find_variable(variable_name)

    def is_var_defined(self, variable_name) -> bool:
        """"Returns True if the Variable is defined"""
        try:
            self.find_variable(variable_name)
            return True
        except:
            return False

    def is_var_local(self, value_name) -> bool:
        """Returns True if the variable is defined in the local scope"""
        return value_name in self.locals

    def create_type(self, name: str) -> Type: # TODO: Revisar la forma de crear tipos. Hasta ahora solo se crea un tipo con el nombre, pero debería tener el resto de la información
        """Creates a type in the Scope
        """
        if name in self.types:
            raise SemanticError(f"Type with the same name ({name}) already in context.")
        type_info = self.types[name] = Type(name)  # Check this
        return type_info

    def get_type(self, name: str) -> Type:  # TODO: Check this
        """Returns the type information"""
        try:
            return self.types[name]
        except:
            raise SemanticError(f'Type "{name}" is not defined.')

    def create_function(self, name, function_pointer: FunctionDeclarationNode) -> Function:
        """Creates a new function in the context"""
        if name in self.function:
            raise SemanticError(f"Function with the same name ({name}) already in context.")

        function = self.function[name] = Function(name, function_pointer)
        return function

    def get_function(self, function_name:str) -> FunctionDeclarationNode:
        """Returns a pointer to the FunctionDeclarationNode of the AST.
        This is useful for interpreting the function"""
        if function_name in self.function:
            return self.function[function_name]
        if not self.parent:
            raise SemanticError(f'The function with name ({function_name}) is not defined')
        return self.parent.get_function(function_name)
    
    def function_defined(self, fname:str) -> bool:
        """Returns True if the function is defined in the context"""
        try:
            self.get_function(fname)
            return True
        except:
            return False

    def create_protocol(self, name, parents): # TODO: Revisar esto de los protocolos
        if name in self.types:
            raise SemanticError(f"Type with the same name ({name}) already in context.")
        protocol = self.types[name] = Protocol(name, parents)
        return protocol

    def __str__(self):
        types_str = (
            "Types: {\n\t"
            + "\n\t".join(y for x in self.types.values() for y in str(x).split("\n"))
            + "\n}"
        )
        func_str = (
            "Functions: {\n\t"
            + "\n\t".join(y for x in self.function.values() for y in str(x).split("\n"))
            + "\n}"
        )
        var_str = (
            "Variables: {\n\t"
            + "\n\t".join(y for x in self.locals.keys() for y in str(x).split("\n"))
            + "\n}"
        )
        return f"{types_str} \n  {func_str} \n {var_str}"
