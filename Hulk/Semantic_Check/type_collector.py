from Hulk.tools.Ast import *
from basic_types.scopes import *
from basic_types.builtin_types import *
from basic_types.builtin_functions import *


def add_basic_types(scope: HulkScopeLinkedNode):
    """
    Agrega los tipos básicos a la tabla de símbolos
    """
    scope.define_type(NoneType())
    scope.define_type(NumType())
    scope.define_type(StringType())
    scope.define_type(BoolType())
    scope.define_type(VectorType())
    scope.define_type(ObjectType())
    scope.define_type(ErrorType())


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
    Agrega las constantes básicas a la tabla de símbolos
    """
    scope.define_variable(VariableInfo("pi", "Number"))
    scope.get_variable("PI").value = math.pi
    scope.define_variable(VariableInfo("e", "Number"))
    scope.get_variable("E").value = math.e

def fill_scope_with_builtin_data(scope: HulkScopeLinkedNode):
    """This function adds all the builtin types, functions and constants to the scope."""
    add_basic_types(scope)
    add_basic_functions(scope)
    add_basic_constants(scope)

class TypeCollector(object):
    """
    Recolecta toda la información relevante de los scopes del hulk
    """

    def __init__(self, scope: HulkScopeLinkedNode, errors: list):
        self.errors = errors if len(errors) >= 0 else []
        self.global_scope: HulkScopeLinkedNode = scope
        add_basic_types(self.global_scope)
        add_basic_functions(self.global_scope)
        add_basic_constants(self.global_scope)
        self.types_to_reprocess = []
        self.functions_to_reprocess = []

    @visitor.on("node")
    def visit(node: AstNode, scope: HulkScopeLinkedNode):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: HulkScopeLinkedNode):
        for declaration in node.declarations:
            self.visit(declaration, self.global_scope)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode, scope: HulkScopeLinkedNode):
        type_constructor_arguments: list[VariableInfo] = [
            get_variable_info_from_var_def(argument)
            for argument in node.constructor_arguments
        ]
        if node.type_name in builtin_types:
            self.errors.append(
                SemanticError(
                    f"Type: {node.type_name} is a built-in type. Cannot redefine it."
                )
            )
            return
        type_info = TypeInfo(node.type_name, type_constructor_arguments)
        features = node.features
        # Create 2 separate list from features. One for AssignNode and one for MethodNode
        attributes: list[AssignNode] = []
        methods: list[MethodNode] = []
        for feature in features:
            if isinstance(feature, AssignNode):
                attributes.append(feature)
            else:
                methods.append(feature)

        # Adds all possible errors when processing attributes and methods
        try:
            type_info.define_attributes(attributes)
        except Exception as e:
            self.errors.append(e)
        try:
            type_info.define_methods(methods)
        except:
            self.errors.append(e)

        try:
            scope.define_type(type_info)
        except Exception as e:
            self.errors.append(e)
            return

        parent_type_id: str = node.parent_type_id
        if parent_type_id in builtin_types:
            self.errors.append(
                SemanticError(
                    f"Type: {node.type_name} cannot inherit from a built-in type"
                )
            )
            return
        if parent_type_id is None:
            node.parent_type_id = "Object"
            parent_type_id = node.parent_type_id
        if parent_type_id == node.type_name:
            self.errors.append(
                SemanticError(f"Type: {node.type_name} cannot inherit from itself")
            )
            return
        if scope.is_type_defined(parent_type_id):
            parent_type = scope.get_type(parent_type_id)
            type_info.set_parent(parent_type)
        else:
            self.types_to_reprocess.append(node)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode, scope: HulkScopeLinkedNode):
        if node.function_name in builtin_functions:
            self.errors.append(
                SemanticError(
                    f"Function: {node.function_name} is a built-in function. Cannot redefine it."
                )
            )
            return
        fix_function_return_type(node)
        if scope.function_defined(node.function_name):
            self.errors.append(
                SemanticError(
                    f"Function: {node.function_name} is already defined in the context."
                )
            )
            return
        function_info = FunctionInfo(
            node.function_name,
            [get_variable_info_from_var_def(argument) for argument in node.arguments],
            node.return_type,
            node,
        )
        try:
            scope.define_function(function_info)
        except Exception as e:
            self.errors.append(e)
            return

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode, scope: HulkScopeLinkedNode):
        pass
