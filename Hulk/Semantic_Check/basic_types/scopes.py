from Hulk.Semantic_Check.basic_types.semantic_types import *
import copy


class HulkScope:
    def __init__(self) -> None:
        self.local_variables: dict[str:VariableInfo] = {}
        """This is a dictionary with all the variables declared in the scope.
        The name of the variable as key and the VariableInfo as value"""
        self.types: dict[str, TypeInfo] = {}
        """This is a dictionary with all the type declarations.
        The name of the type as key and the TypeInfo as value"""
        self.protocols: dict[str, ProtocolInfo] = {}
        """This is a dictionary with all the protocol declarations.
        The name of the protocol as key and the ProtocolInfo as value"""
        self.functions: dict[str, FunctionInfo] = {}
        """This is a dictionary with all the function declarations.
        The name of the function as key and the FunctionInfo as value"""

    def clone(self) -> Self:
        return copy.deepcopy(self)


class HulkScopeLinkedNode:
    def __init__(self, parent: Self = None):
        super().__init__()
        self.parent: HulkScopeLinkedNode = parent
        """This is a reference to the parent scope"""
        self.children = []
        self.scope: HulkScope = HulkScope()
        """This is the scope of this node"""

    def define_variable(
            self, variable_info: VariableInfo, clone: bool = False
    ) -> VariableInfo:
        """Create a new variable in the actual scope"""
        if variable_info.name in self.scope.local_variables:
            raise SemanticError(
                f"The variable: {variable_info.name} is already defined"
            )
        info = variable_info.clone() if clone else variable_info
        self.scope.local_variables[info.name] = info
        return info

    def get_variable(self, variable_name: str) -> VariableInfo:
        """Try to find the variable in the local scope and if it is not in here
        it tries to find it in the parent scope.
        And if the variable is not in any of the parent scopes it raise a semantic error
        """
        if variable_name in self.scope.local_variables:
            return self.scope.local_variables[variable_name]
        if not self.parent:
            raise SemanticError(f"The variable ({variable_name}) is not defined")
        return self.parent.get_variable(variable_name)

    def is_var_defined(self, variable_name: str) -> bool:
        """ "Returns True if the Variable is defined"""
        try:
            self.get_variable(variable_name)
            return True
        except:
            return False

    def is_var_local(self, value_name: str) -> bool:
        """Returns True if the variable is defined in the local scope"""
        return value_name in self.scope.local_variables

    def define_type(
            self,
            type_name: str,
    ) -> TypeInfo:
        """Create a new type in the actual scope"""
        if type_name in self.scope.types:
            raise SemanticError(f"The type: {type_name} is already defined")
        new_type = TypeInfo(type_name)
        self.scope.types[type_name] = new_type
        return new_type

    def define_type_by_instance(
            self, type_info: TypeInfo, clone: bool = False
    ) -> TypeInfo:
        """Create a new type in the actual scope"""
        if type_info.name in self.scope.types:
            raise SemanticError(f"The type: {type_info.name} is already defined")
        result = type_info if not clone else type_info.clone()
        self.scope.types[type_info.name] = result
        return result

    def is_type_defined(self, type_name: str) -> bool:
        """Returns True if the type is defined in the context"""
        if type_name in self.scope.types:
            return True
        if not self.parent:
            return False
        return self.parent.is_type_defined(type_name)

    def get_type(self, name: str) -> TypeInfo:  # TODO: Check this
        """Returns the type information"""
        if name in self.scope.types:
            return self.scope.types[name]
        if not self.parent:
            raise SemanticError(f"The type ({name}) is not defined")
        return self.parent.get_type(name)

    def define_function(
            self, function_info: FunctionInfo, clone: bool = False
    ) -> FunctionInfo:
        """Creates a new function in the context"""
        if function_info.name in self.scope.functions:
            raise SemanticError(
                f"Function with the same name ({function_info.name}) already in the Context."
            )
        result = function_info if not clone else function_info.clone()
        self.scope.functions[result.name] = result
        return result

    def get_function(self, function_name: str) -> FunctionInfo:
        """Returns the FunctionInfo associated with that name"""
        if function_name in self.scope.functions:
            return self.scope.functions[function_name]
        if not self.parent:
            raise SemanticError(
                f"The function with name ({function_name}) is not defined"
            )
        return self.parent.get_function(function_name)

    def is_function_defined(self, function_name: str) -> bool:
        """Returns True if the function is defined in the context"""
        if function_name in self.scope.functions:
            return True
        if not self.parent:
            return False
        return self.parent.is_function_defined(function_name)

    def define_protocol(self, name: str):
        """This method defines a new protocol if it has not been added before to the scope"""
        if name in self.scope.protocols:
            raise SemanticError(f"Type with the same name ({name}) already in context.")
        protocol = ProtocolInfo(name)
        self.scope.protocols[name] = protocol
        return protocol

    def define_protocol_by_instance(self, protocol_info: ProtocolInfo):
        """This method defines a new protocol if it has not been added before to the scope"""
        if protocol_info.name in self.scope.protocols:
            raise SemanticError(
                f"Type with the same name ({protocol_info.name}) already in context."
            )
        self.scope.protocols[protocol_info.name] = protocol_info
        return protocol_info

    def is_protocol_defined(self, protocol_name: str) -> bool:
        """Returns True if the protocol is defined in the context"""
        if protocol_name in self.scope.protocols:
            return True
        if not self.parent:
            return False
        return self.parent.is_protocol_defined(protocol_name)

    def get_protocol(self, protocol_name: str) -> ProtocolInfo:
        """Returns the protocol information"""
        if protocol_name in self.scope.protocols:
            return self.scope.protocols[protocol_name]
        if not self.parent:
            raise SemanticError(f"The protocol ({protocol_name}) is not defined")
        return self.parent.get_protocol(protocol_name)

    def get_all_types_names(self) -> list[str]:
        return list(self.scope.types.keys())

    def __str__(self):
        types_str = (
                "Types: {\n\t"
                + "\n\t".join(
            y for x in self.scope.types.values() for y in str(x).split("\n")
        )
                + "\n}"
        )
        func_str = (
                "Functions: {\n\t"
                + "\n\t".join(y for x in self.function.values() for y in str(x).split("\n"))
                + "\n}"
        )
        var_str = (
                "Variables: {\n\t"
                + "\n\t".join(
            y for x in self.scope.local_variables.keys() for y in str(x).split("\n")
        )
                + "\n}"
        )
        return f"{types_str} \n  {func_str} \n {var_str}"
