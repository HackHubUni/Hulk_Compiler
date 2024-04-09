from Hulk.tools.Ast import *
from Hulk.Semantic_Check.basic_types.scopes import *
from Hulk.Semantic_Check.basic_types.builtin_types import *
from Hulk.Semantic_Check.basic_types.builtin_functions import *
from Hulk.Semantic_Check.basic_types.builtin_protocols import *
from Hulk.Semantic_Check.basic_types.semantic_types import *
from Hulk.Semantic_Check.utils import *


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

    def check_arguments(
        self,
        arguments: list[VarDefNode],
        scope: HulkScopeLinkedNode,
        from_where: str,
    ) -> list[VariableInfo]:
        """Check if the VarDefNode of the arguments are unique and if their types exists.
        Updates the errors and return a list of VariableInfo"""
        return_arguments: list[VariableInfo] = []
        args_names: set[str] = set()
        for var_def in arguments:
            # Check if names are unique
            if var_def.var_name in args_names:
                self.errors.append(
                    SemanticError(
                        f"{from_where}, the argument '{var_def.var_name}' is already defined"
                    )
                )
                var_def.var_name = get_unique_name_with_guid(var_def.var_name)
            # Check if the type of the argument exists
            if not scope.is_type_or_protocol_defined(var_def.var_type):
                error = SemanticError(
                    f"{from_where}, in the parameter '{var_def.var_name}', there is no type or protocol defined with the name '{var_def.var_type}'"
                )
                self.errors.append(error)
                var_def.var_type = NoneType.static_name()
            var_info = get_variable_info_from_var_def(var_def)
            return_arguments.append(var_info)
            args_names.add(var_def.var_name)
        return return_arguments

    @visitor.on("node")
    def visit(self, node, scope: HulkScopeLinkedNode, from_where: str = ""):
        pass

    @visitor.when(ProgramNode)
    def visit(
        self,
        node: ProgramNode,
        scope: HulkScopeLinkedNode,
        from_where: str = "In the program,",
    ):
        for declaration in node.declarations:
            self.visit(declaration, self.global_scope, from_where)

    @visitor.when(TypeDeclarationNode)
    def visit(
        self,
        node: TypeDeclarationNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ):
        from_where += f" in the declaration of the type '{node.type_name}',"
        # get the TypeInfo from the scope
        type_info: TypeInfo = scope.get_type(node.type_name)
        self.current_type = type_info
        constructor_arguments: list[VarDefNode] = node.constructor_arguments

        # Check if the constructor arguments are valid
        arguments = self.check_arguments(
            constructor_arguments,
            scope,
            f"{from_where} in it's constructor '{node.type_name}'",
        )

        type_info.set_constructor_arguments(arguments)

        type_info.set_parent_initialization_expressions(
            node.parent_initialization_expressions
        )

        # Check if parent exists
        if not scope.is_type_defined(node.parent_type_id):
            error = SemanticError(
                f"{from_where} there is no type defined with the name '{node.parent_type_id}' for inheritance"
            )
            self.errors.append(error)
            node.parent_type_id = ObjectType.static_name()

        parent_type: TypeInfo = scope.get_type(node.parent_type_id)

        # Check if parent is a builtin type
        if is_builtin_type(parent_type):
            error = SemanticError(
                f"{from_where} the type '{node.parent_type_id}' is a builtin type that cannot be used as a parent type"
            )
            self.errors.append(error)
            node.parent_type_id = ObjectType.static_name()
            parent_type = scope.get_type(node.parent_type_id)

        # Add the parent to the type
        type_info.set_parent(parent_type)

        features = node.features
        # iterate over the features of the type
        for feature in features:
            self.visit(feature, scope, from_where)

    @visitor.when(ProtocolDeclarationNode)
    def visit(
        self,
        node: ProtocolDeclarationNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ):
        from_where += f" in the declaration of the protocol '{node.protocol_name}',"
        # get the ProtocolInfo from the scope
        protocol_info: ProtocolInfo = scope.get_protocol(node.protocol_name)
        # In this pass is not possible to check for cyclic inheritance of protocols because is in this pass where we assign the immediate parent

        if node.parent:
            if not scope.is_protocol_defined(node.parent):
                error = SemanticError(
                    f"{from_where} there is no protocol defined with the name '{node.parent}' that could be used as parent"
                )
                self.errors.append(error)
                node.parent = None
                protocol_info.parent = node.parent
            else:
                protocol_info.parent = scope.get_protocol(node.parent)
        self.current_protocol = protocol_info
        # iterate over the methods of the protocol
        for method in node.methods:
            self.visit(method, scope, from_where)

    @visitor.when(FunctionDeclarationNode)
    def visit(
        self,
        node: FunctionDeclarationNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ):
        from_where += f" in the declaration of the function '{node.function_name}',"
        # get the FunctionInfo from the scope
        function_info: FunctionInfo = scope.get_function(node.function_name)
        # Check the arguments of the function
        func_declaration: FunctionDeclarationNode = function_info.function_pointer
        arguments: list[VariableInfo] = self.check_arguments(
            func_declaration.arguments, scope, from_where
        )
        function_info.arguments = arguments

        # Check if the return type exists
        if not scope.is_type_or_protocol_defined(function_info.return_type):
            error = SemanticError(
                f"In the return type of the function '{node.function_name}', there is no type or protocol defined with the name '{function_info.return_type}'"
            )
            self.errors.append(error)
            node.return_type = NoneType.static_name()
            function_info.return_type = node.return_type

    @visitor.when(MethodNode)
    def visit(
        self,
        node: MethodNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ):
        """This method is executed for processing the declaration of a method
        inside a type. This type is stored in the variable self.current_type"""
        # This method should add the TypeMethodInfo to the current type
        from_where += f" in the declaration of the method '{node.method_name}',"
        current_type: TypeInfo = self.current_type
        method_name: str = node.method_name
        # Check if the method is defined in the type
        if current_type.is_method_defined(method_name):
            error = SemanticError(
                f"{from_where} there is another method defined with the same name"
            )
            self.errors.append(error)
            # Give a new name to the method
            method_name = node.method_name = get_unique_name_with_guid(method_name)

        # Check the arguments
        arguments = self.check_arguments(
            node.arguments, scope, f"In the method '{method_name}'"
        )

        # Fix the return type to NoneType if there is no type annotated in the return type of the method
        fix_method_return_type(node)

        if not scope.is_type_or_protocol_defined(node.return_type):
            error = SemanticError(
                f"{from_where}, in the return type, there is no type or protocol defined with the name '{node.return_type}'"
            )
            self.errors.append(error)
            node.return_type = NoneType.static_name()

        current_type.define_method(
            TypeMethodInfo(method_name, arguments, node.return_type, node)
        )

    @visitor.when(AssignNode)
    def visit(
        self,
        node: AssignNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ):
        """This method is executed for processing the assignment of a variable
        inside a type. This type is stored in the variable self.current_type"""
        from_where += f" in the assignment of the attribute with name '{node.var_definition.var_name}',"
        current_type: TypeInfo = self.current_type
        var_definition: VarDefNode = node.var_definition
        var_name: str = var_definition.var_name
        if current_type.is_attribute_defined(var_name):
            error = SemanticError(
                f"{from_where} the name '{var_name}' is already in another attribute"
            )
            self.errors.append(error)
            var_name = var_definition.var_name = get_unique_name_with_guid(var_name)
        var_info: VariableInfo = get_variable_info_from_var_def(var_definition)
        if not scope.is_type_or_protocol_defined(var_definition.var_type):
            error = SemanticError(
                f"{from_where} there is no type or protocol defined with the name '{var_definition.var_type}'"
            )
            self.errors.append(error)
            var_definition.var_type = NoneType.static_name()
            var_info.type = var_definition.var_type
        var_info.initialization_expression = node.expression_to_evaluate
        current_type.define_attribute(var_info)

    @visitor.when(ProtocolMethodNode)
    def visit(
        self,
        node: ProtocolMethodNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ):
        """This method is executed for processing the declaration of a method
        inside a protocol. This protocol type is stored in the variable self.current_protocol
        """
        from_where += (
            f" in the declaration of the protocol method '{node.protocol_method_name}',"
        )
        current_protocol: ProtocolInfo = self.current_protocol
        protocol_method_name: str = node.protocol_method_name
        # Check if the method is defined in the protocol
        if current_protocol.is_method_defined(protocol_method_name, local=True):
            error = SemanticError(
                f"{from_where} there is another method defined with the same name"
            )
            self.errors.append(error)
            # Give a new name to the method
            node.protocol_method_name = get_unique_name_with_guid(protocol_method_name)
            protocol_method_name = node.protocol_method_name
        # Check the arguments of the protocol method
        arguments: list[VariableInfo] = self.check_arguments(
            node.arguments, scope, from_where
        )
        protocol_method = MethodInfoBase(protocol_method_name, arguments, node)
        # Check the return type of the protocol method
        if not scope.is_type_or_protocol_defined(node.return_type):
            error = SemanticError(
                f"{from_where} in the return type, there is no type defined with the name '{node.return_type}'"
            )
            self.errors.append(error)
            node.return_type = ErrorType.static_name()
        protocol_method.return_type = node.return_type
        current_protocol.define_method(protocol_method)
