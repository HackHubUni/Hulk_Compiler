from Hulk.tools.Ast import *
from basic_types.scopes import *
from basic_types.builtin_types import *
from basic_types.builtin_functions import *
from basic_types.builtin_protocols import *


def add_basic_types(scope: HulkScopeLinkedNode):
    """
    Agrega los tipos básicos a la tabla de símbolos
    """
    scope.define_type_by_instance(NoneType())
    scope.define_type_by_instance(NumType())
    scope.define_type_by_instance(StringType())
    scope.define_type_by_instance(BoolType())
    scope.define_type_by_instance(VectorType())
    scope.define_type_by_instance(ObjectType())
    scope.define_type_by_instance(ErrorType())


def add_basic_functions(scope: HulkScopeLinkedNode):
    """
    Agrega las funciones básicas a la tabla de símbolos
    """
    scope.define_function(SinFunction())
    scope.define_function(CosFunction())
    scope.define_function(SqrtFunction())
    scope.define_function(LogFunction())
    scope.define_function(ExponentialFunction())
    scope.define_function(RandomFunction())


def add_basic_constants(scope: HulkScopeLinkedNode):
    """
    Adds the basic constants to the scope
    """
    scope.define_variable(VariableInfo("pi", "Number"))
    scope.get_variable("PI").value = math.pi
    scope.define_variable(VariableInfo("e", "Number"))
    scope.get_variable("E").value = math.e


def add_basic_protocols(scope: HulkScopeLinkedNode):
    """Adds the builtin protocols to the scope"""
    scope.define_protocol_by_instance(IterableProtocol())


def fill_scope_with_builtin_data(scope: HulkScopeLinkedNode):
    """This function adds all the builtin types, functions and constants to the scope."""
    add_basic_types(scope)
    add_basic_functions(scope)
    add_basic_protocols(scope)
    add_basic_constants(scope)


class TypeCollector(object):
    """
    Collects all the types and protocols defined in the program.
    It also adds all the builtin types, protocols, functions and constants
    """

    def __init__(self, scope: HulkScopeLinkedNode, errors: list):
        self.errors = errors if len(errors) >= 0 else []
        self.global_scope: HulkScopeLinkedNode = scope
        fill_scope_with_builtin_data(self.global_scope)

    @visitor.on("node")
    def visit(node: AstNode, scope: HulkScopeLinkedNode):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: HulkScopeLinkedNode):
        for declaration in node.declarations:
            self.visit(declaration, self.global_scope)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode, scope: HulkScopeLinkedNode):
        if node.type_name in builtin_types:
            self.errors.append(
                SemanticError(
                    f"Type {node.type_name} is a builtin type and cannot be redefined"
                )
            )
            node.type_name = get_name_with_added_error(node.type_name)
        elif scope.is_type_defined(node.type_name):
            self.errors.append(
                SemanticError(f"Type {node.type_name} is already defined")
            )
            node.type_name = get_name_with_added_error(node.type_name)
        scope.define_type(node.type_name)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode, scope: HulkScopeLinkedNode):
        if node.protocol_name in builtin_protocols:
            self.errors.append(
                SemanticError(
                    f"Protocol {node.protocol_name} is a builtin protocol and cannot be redefined"
                )
            )
            node.protocol_name = get_name_with_added_error(node.protocol_name)
        elif scope.is_protocol_defined(node.protocol_name):
            self.errors.append(
                SemanticError(f"Protocol {node.protocol_name} is already defined")
            )
            node.protocol_name = get_name_with_added_error(node.protocol_name)
        scope.define_protocol(node.protocol_name)
