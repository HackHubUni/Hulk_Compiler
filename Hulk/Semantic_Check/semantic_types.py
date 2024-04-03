# from cmp.semantic import *
from semantic_errors import *
from instance_types import *
from collections import OrderedDict
from Hulk.tools.Ast import *
from abc import ABC
from Hulk.tools.Ast import *


class MethodInfo:
    def __init__(
        self,
        name: str,
        params: list[VariableInfo],
        return_type: str,
        declaration_node_pointer: MethodNode,
    ):
        self.name: str = name
        """This is the name of the method"""
        self.param_names: list[VariableInfo] = params
        """This is a list of VariableInfo and stores the basic information of the parameters of the method"""
        self.return_type: str = return_type
        """This is the name of the return type"""
        self.declaration_pointer: MethodNode = declaration_node_pointer
        """This is the pointer to the AST node where the Method is declared"""

    def __str__(self):
        params = ", ".join(str(var_info) for var_info in self.param_names)
        return f"[method] {self.name}({params}): {self.return_type.name};"

    def __eq__(self, other):
        eq = lambda x, y: x == y
        if not isinstance(other, MethodInfo):
            return False
        return (
            other.name == self.name
            and other.return_type == self.return_type
            and len(other.param_names) == len(self.param_names)
            and all(
                eq(element[0], element[1])
                for element in zip(other.param_names, self.param_names)
            )
        )


class TypeInfo:
    def __init__(self, name: str):
        self.name = name
        """The name of the Type"""
        self.attributes: dict[str, VariableInfo] = {}
        """The dictionary of the variables"""
        self.methods: dict[str, MethodInfo] = {}
        """The dictionary of the methods"""
        self.parent: str = None
        """The parent type name"""

    def create_instance(self) -> TypeInstance:
        """Returns a instance of this type. That is nothing more that a clone of the attributes"""
        return TypeInstance(
            self.name, [instance[1].clone() for instance in self.attributes.items()]
        )

    def set_parent(self, parent: str):
        """Tries of changing the type of the parent. Raise an SemanticError if the type of the parent was already set"""
        if self.parent is not None or self.parent != "":
            raise SemanticError(
                f"Parent type is already set for {self.name}. It's value is {self.parent}"
            )
        self.parent = parent

    def get_attribute(self, name: str) -> VariableInfo:
        """Returns the attribute with this name. If not found raise a SemanticError"""
        if name in self.attributes:
            return self.attributes[name]
        raise SemanticError(
            f"The type ({self.name}) has no attribute with name ({name})"
        )

    def define_new_attribute(self, attribute: VariableInfo):
        if attribute.name in self.attributes:
            raise SemanticError(
                f"An attribute with name '{attribute.name}' is already defined in the type '{self.name}'"
            )
        self.attributes[attribute.name] = attribute.clone()

    def get_method(self, name: str):
        if name in self.methods:
            return self.methods[name]
        raise SemanticError(
            f"There is no method named '{name}' in the type '{self.name}'"
        )

    def define_method(
        self,
        name: str,
        params: list[VariableInfo],
        return_type: str,
        method_declaration_pointer: MethodNode,
    ):
        """Define a new method in the Type. If a method with the same name is already defined then it raise a SemanticError"""
        if name in self.methods:
            raise SemanticError(
                f"I the type '{self.name}' there is already a definition for a method with name"
            )
        method = MethodInfo(name, params, return_type, method_declaration_pointer)
        self.methods[name] = method

    def all_attributes(self) -> list[VariableInfo]:
        """Returns a list with all the attributes in the type"""
        return list(item[1] for item in self.attributes.items())

    def all_methods(self) -> list[MethodInfo]:
        return list(item[1] for item in self.methods.items())

    def conforms_to(self, other):
        return (
            other.bypass()
            or self == other
            or self.parent is not None
            and self.parent.conforms_to(other)
        )

    def bypass(self):
        return False

    def __str__(self):
        output = f"type {self.name}"
        parent = "" if self.parent is None else f" : {self.parent.name}"
        output += parent
        output += " {"
        output += "\n\t" if self.attributes or self.methods else ""
        output += "\n\t".join(str(x) for x in self.attributes)
        output += "\n\t" if self.attributes else ""
        output += "\n\t".join(str(x) for x in self.methods)
        output += "\n" if self.methods else ""
        output += "}\n"
        return output

    def __repr__(self):
        return str(self)


class FunctionInfo:
    def __init__(
        self,
        name: str,
        param_names: list[VariableInfo],
        return_type: str,
        function_pointer: FunctionDeclarationNode,
    ):
        self.name: str = name
        """The name of the function"""
        self.param_names: list[VariableInfo] = param_names
        """This is the list of Variable Info that represents each parameter of the function.
        The variable info contains information like the name of the variable and the type asociated"""
        self.return_type: str = return_type
        """This is the string with the name of the type"""
        self.function_pointer: FunctionDeclarationNode = function_pointer
        """This is the pointer to the AST where the Function is declared.
        It is needed for the step of interpreting the tree"""

    def __str__(self):
        output = f"function {self.name}"
        output += " ("
        params = ", ".join(f"{n.id}:{n.type.name}" for n in self.param_names)
        output += params
        output += ") :"
        output += self.return_type.name
        return output

    def __eq__(self, other: TypeInfo):
        return (
            other.name == self.name and other.return_type == self.return_type
        )  # and \
        # other.param_types == self.param_types


class ProtocolInfo:
    def __init__(
        self,
        name: str,
    ):
        self.name = name
        self.methods = []

    def define_method(
        self, name: str, param_names: list, param_types: list, return_type
    ):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = MethodInfo(name, param_names, param_types, return_type)
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
