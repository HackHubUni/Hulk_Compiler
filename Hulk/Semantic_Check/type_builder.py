from Hulk.tools.Ast import *
from basic_types.scopes import *
from basic_types.builtin_types import *
from basic_types.builtin_functions import *
from basic_types.builtin_protocols import *
from basic_types.semantic_types import *


class TypeBuilder:
    """This class constructs all the types, protocols and functions of a program.
    Also constructs all the attributes and methods of the types and protocols"""

    def __init__(self, scope: HulkScopeLinkedNode, errors: list) -> None:
        self.global_scope: HulkScopeLinkedNode = scope
        """This is the global scope of the program. Containing all the declarations"""
        self.errors = errors if len(errors) >= 0 else []
        """All the errors that the program contains"""
        self.current_type: TypeInfo = None
        """The current type that is been processed"""
        self.current_protocol: ProtocolInfo = None
        """The current protocol that is been processed"""

    @visitor.on("node")
    def visit(self, node: AstNode, scope: HulkScopeLinkedNode):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: HulkScopeLinkedNode):
        for declaration in node.declarations:
            self.visit(declaration, self.global_scope)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode, scope: HulkScopeLinkedNode):
        # get the TypeInfo from the scope
        type_info: TypeInfo = scope.get_type(node.type_name)
        self.current_type = type_info
        constructor_arguments: list[VarDefNode] = node.constructor_arguments
        # iterate over the constructor arguments and add it to the type
        for argument in constructor_arguments:
            arg_type = scope.get_type(argument.var_type)
            try:
                var = get_variable_info_from_var_def(argument)
                var.type_name = arg_type
                type_info.add_constructor_argument(var)
                break
            except Exception as e:
                self.errors.append(e)
                argument.var_name = get_unique_name_with_guid(argument.var_name)

        type_info.set_parent_initialization_expressions(
            node.parent_initialization_expressions
        )
        features = node.features
        # iterate over the features of the type
        for feature in features:
            self.visit(feature, scope)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode, scope: HulkScopeLinkedNode):
        # get the ProtocolInfo from the scope
        protocol_info: ProtocolInfo = scope.get_protocol(node.protocol_name)
        self.current_protocol = protocol_info
        # iterate over the methods of the protocol
        for method in node.methods:
            self.visit(method, scope)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode, scope: HulkScopeLinkedNode):
        # get the FunctionInfo from the scope
        function_info: FunctionInfo = scope.get_function(node.function_name)
        # iterate over the arguments of the function
        for argument in function_info.arguments:
            if not scope.is_type_defined(argument.type_name):
                error = SemanticError(
                    f"In the function '{node.function_name}', in the parameter '{argument.name}', there is no type defined with the name '{argument.type_name}'"
                )
                self.errors.append(error)
        if not scope.is_type_defined(function_info.return_type):
            error = SemanticError(
                f"In the return type of the function '{node.function_name}', there is no type defined with the name '{function_info.return_type}'"
            )
            self.errors.append(error)

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the declaration of a method
        inside a type. This type is stored in the variable self.current_type"""
        # This method should add the TypeMethodInfo to the current type
        current_type: TypeInfo = self.current_type
        method_name = node.method_name
        if current_type.is_method_defined(method_name):
            error = SemanticError(
                f"The method '{method_name}' is already defined in the type '{current_type.type_id}'"
            )
            self.errors.append(error)
            # Give a new name to the method
            method_name = node.method_name = get_unique_name_with_guid(method_name)
        arguments: list[VariableInfo] = [
            get_variable_info_from_var_def(arg) for arg in node.arguments
        ]
        fix_method_return_type(node)
        current_type.add_method(TypeMethodInfo(method_name, arguments, node.return_type, node))
        

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the assignment of a variable
        inside a type. This type is stored in the variable self.current_type"""
        pass

    @visitor.when(ProtocolMethodNode)
    def visit(self, node: ProtocolMethodNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the declaration of a method
        inside a protocol. This protocol type is stored in the variable self.current_protocol
        """
        pass
