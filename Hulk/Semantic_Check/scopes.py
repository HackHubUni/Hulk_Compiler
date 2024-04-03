from semantic_types import *


class HulkScopeBase:
    def __init__(self) -> None:
        self.locals: dict[str:VariableInfo] = {}  # TODO
        self.children = []
        self.types: dict[str, TypeInfo] = {}
        self.function: dict[str, FunctionInfo] = {}


class HulkScope(HulkScopeBase):
    def __init__(self, parent: HulkScopeBase):
        super().__init__()
        self.parent: HulkScope = parent

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
        """ "Returns True if the Variable is defined"""
        try:
            self.find_variable(variable_name)
            return True
        except:
            return False

    def is_var_local(self, value_name) -> bool:
        """Returns True if the variable is defined in the local scope"""
        return value_name in self.locals

    def create_type(
        self, name: str
    ) -> (
        TypeInfo
    ):  # TODO: Revisar la forma de crear tipos. Hasta ahora solo se crea un tipo con el nombre, pero debería tener el resto de la información
        """Creates a type in the Scope"""
        if name in self.types:
            raise SemanticError(f"Type with the same name ({name}) already in context.")
        type_info = self.types[name] = TypeInfo(name)  # Check this
        return type_info

    def get_type(self, name: str) -> TypeInfo:  # TODO: Check this
        """Returns the type information"""
        try:
            return self.types[name]
        except:
            raise SemanticError(f'Type "{name}" is not defined.')

    def create_function(
        self, name, function_pointer: FunctionDeclarationNode
    ) -> FunctionInfo:
        """Creates a new function in the context"""
        if name in self.function:
            raise SemanticError(
                f"Function with the same name ({name}) already in context."
            )

        function = self.function[name] = FunctionInfo(name, function_pointer)
        return function

    def get_function(self, function_name: str) -> FunctionDeclarationNode:
        """Returns a pointer to the FunctionDeclarationNode of the AST.
        This is useful for interpreting the function"""
        if function_name in self.function:
            return self.function[function_name]
        if not self.parent:
            raise SemanticError(
                f"The function with name ({function_name}) is not defined"
            )
        return self.parent.get_function(function_name)

    def function_defined(self, fname: str) -> bool:
        """Returns True if the function is defined in the context"""
        try:
            self.get_function(fname)
            return True
        except:
            return False

    def create_protocol(self, name, parents):  # TODO: Revisar esto de los protocolos
        if name in self.types:
            raise SemanticError(f"Type with the same name ({name}) already in context.")
        protocol = self.types[name] = ProtocolInfo(name, parents)
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
