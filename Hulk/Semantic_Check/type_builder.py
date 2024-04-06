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
                        f"The argument '{var_def.var_name}' is already defined"
                    )
                )
                var_def.var_name = get_unique_name_with_guid(var_def.var_name)
            var_info = get_variable_info_from_var_def(
                var_def
            )  # This line fix the empty or None return type
            # Check if the type of the argument exists
            if not scope.is_type_defined(var_def.var_type):
                error = SemanticError(
                    f"{from_where}, in the parameter '{var_def.var_name}', there is no type defined with the name '{var_def.var_type}'"
                )
                self.errors.append(error)
                var_def.var_type = ErrorType.static_name()
            return_arguments.append(var_info)
            args_names.add(var_def.var_name)
        return return_arguments

    @visitor.on("node")
    def visit(self, node, scope: HulkScopeLinkedNode):
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

        arguments = self.check_arguments(
            constructor_arguments,
            scope,
            f"In the constructor argument of the type '{node.type_name}'",
        )

        type_info.set_constructor_arguments(arguments)

        type_info.set_parent_initialization_expressions(
            node.parent_initialization_expressions
        )

        if not scope.is_type_defined(node.parent_type_id):
            error = SemanticError(
                f"In the type '{node.type_name}', there is no type defined with the name '{node.parent_type_id}'"
            )
            self.errors.append(error)
            node.parent_type_id = ErrorType.static_name()

        parent_type = scope.get_type(node.parent_type_id)

        if is_builtin_type(parent_type):
            error = SemanticError(
                f"The type '{node.parent_type_id}' is a builtin type that cannot be used as a parent type"
            )
            self.errors.append(error)
            parent_type = scope.get_type(ErrorType.static_name())
        if parent_type.name == NoneType.static_name():
            parent_type = scope.get_type(ObjectType.static_name())
        type_info.set_parent(parent_type)
        features = node.features

        # TODO: Check if this could be moved to the next section of the Semantic Checker
        # Check if the length of the parent initialization expression match the length of the parent arguments
        if len(node.parent_initialization_expressions) != len(
            parent_type.constructor_arguments
        ):
            error = SemanticError(
                f"In the type '{node.type_name}', the number of arguments in the parent initialization expression does not match the number of arguments in the parent type '{node.parent_type_id} declaration'"
            )
            self.errors.append(error)

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
            # Check types of the arguments to see if they exists. The names are unique. This is ensured by the TypeCollector
            if not scope.is_type_defined(argument.type):
                error = SemanticError(
                    f"In the function '{node.function_name}', in the parameter '{argument.name}', there is no type defined with the name '{argument.type}'"
                )
                self.errors.append(error)
                # FIXME: There is an error in here. We should modify the type of this Ast Node but right now is not possible because of the previous semantic pass
        # Check if the return type exists
        if not scope.is_type_defined(function_info.return_type):
            error = SemanticError(
                f"In the return type of the function '{node.function_name}', there is no type defined with the name '{function_info.return_type}'"
            )
            self.errors.append(error)
            # FIXME: This one should be fixed too

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the declaration of a method
        inside a type. This type is stored in the variable self.current_type"""
        # This method should add the TypeMethodInfo to the current type
        current_type: TypeInfo = self.current_type
        method_name = node.method_name
        # Check if the method is defined in the type
        if current_type.is_method_defined(method_name):
            error = SemanticError(
                f"The method '{method_name}' is already defined in the type '{current_type.type_id}'"
            )
            self.errors.append(error)
            # Give a new name to the method
            method_name = node.method_name = get_unique_name_with_guid(method_name)

        arguments = self.check_arguments(
            node.arguments, scope, f"In the method '{method_name}'"
        )

        fix_method_return_type(node)

        if not scope.is_type_defined(node.return_type):
            error = SemanticError(
                f"In the method '{method_name}', there is no type defined with the name '{node.return_type}'"
            )
            self.errors.append(error)
            node.return_type = ErrorType.static_name()

        current_type.define_method(
            TypeMethodInfo(method_name, arguments, node.return_type, node)
        )

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the assignment of a variable
        inside a type. This type is stored in the variable self.current_type"""
        # TODO: Find out what to do with the Expression Initialization of the variable. Remember this is necessary for the interpreter
        current_type = self.current_type
        var_definition: VarDefNode = node.var_definition
        var_name: str = var_definition.var_name
        if current_type.is_attribute_defined(var_name):
            error = SemanticError(
                f"The attribute '{var_name}' is already defined in the type '{current_type.name}'"
            )
            self.errors.append(error)
            var_name = var_definition.var_name = get_unique_name_with_guid(var_name)
        var_info = get_variable_info_from_var_def(var_definition)
        if not scope.is_type_defined(var_definition.var_type):
            error = SemanticError(
                f"In the type '{current_type.name}', in the attribute '{var_name}', there is no type defined with the name '{var_definition.var_type}'"
            )
            self.errors.append(error)
            var_info.type = var_definition.var_type = ErrorType.static_name()
        var_info.initialization_expression = node.expression_to_evaluate
        current_type.define_attribute(var_info)

    @visitor.when(ProtocolMethodNode)
    def visit(self, node: ProtocolMethodNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the declaration of a method
        inside a protocol. This protocol type is stored in the variable self.current_protocol
        """
        current_protocol = self.current_protocol
        protocol_method_name = node.protocol_method_name
        # Check if the name of the protocol method is already defined
        if current_protocol.is_method_defined(protocol_method_name):
            error = SemanticError(
                f"The method '{protocol_method_name}' is already defined in the protocol '{current_protocol.protocol_id}'"
            )
            self.errors.append(error)
            # Give a new name to the method with a GUID
            protocol_method_name = node.protocol_method_name = (
                get_unique_name_with_guid(protocol_method_name)
            )
        arguments: list[VariableInfo] = self.check_arguments(
            node.arguments, scope, f"In the method '{protocol_method_name}'"
        )
        fix_method_return_type(node)
        if not scope.is_type_defined(node.return_type):
            error = SemanticError(
                f"In the protocol '{current_protocol.name}', in the method '{protocol_method_name}', there is no type defined with the return type name '{node.return_type}'"
            )
            self.errors.append(error)
            node.return_type = ErrorType.static_name()

        current_protocol.define_method(
            MethodInfoBase(protocol_method_name, arguments, node.return_type)
        )
