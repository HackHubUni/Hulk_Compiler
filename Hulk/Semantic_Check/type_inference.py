from Hulk.tools.Ast import *
from Hulk.Semantic_Check.basic_types.scopes import *
from Hulk.Semantic_Check.basic_types.builtin_types import *
from Hulk.Semantic_Check.basic_types.builtin_functions import *
from Hulk.Semantic_Check.basic_types.builtin_protocols import *
from Hulk.Semantic_Check.basic_types.semantic_types import *

# NOTE: When this class gets executed it is assumed that all the types, functions and protocols are already in the scope


class TypeInference:
    """This class executes the type inference of the Hulk program.
    It will modify the Tree to annotate each node with the corresponding type."""

    def __init__(self, scope: HulkScopeLinkedNode, errors: list):
        self.global_scope: HulkScopeLinkedNode = scope
        """The global scope of the Hulk program"""
        self.errors = errors if errors is not None and len(errors) >= 0 else []
        """The list of errors previously found in the program"""

    def visit_expects(
        self,
        node: ExpressionNode,
        scope: HulkScopeLinkedNode,
        expected_return_value: TypeInfo,
        from_where: str,
    ) -> TypeInfo:
        """This function calls the visit on the node given. But is useful to call this instead of the visit function in the cases
        where there exist an expected return type from the visit. This will be used by the operators in the language
        and by the function and method arguments
        """
        # TODO: Think about the case of expected_return_value been the NoneType
        expression_type = self.visit(node, scope, from_where)
        if isinstance(expression_type, ErrorType):
            return expression_type
        if isinstance(node, FunctionCallNode):
            try:
                function_info = scope.get_function(node.function_id)
                if isinstance(function_info, BuiltinFunction):
                    return expression_type
                func_decl = function_info.function_pointer
                if scope.get_type(func_decl.return_type):
                    pass
            except:
                pass
        elif isinstance(node, MethodCallWithIdentifierNode):
            pass
        elif isinstance(node, MethodCallWithExpressionNode):
            pass
        elif isinstance(node, VarNode):
            pass
        elif isinstance(node, VarDefNode):
            pass
        # AttrCall is not analyzed here because always have a type when the TypeDeclarationNode is processed.
        if not expression_type.conforms_to(expected_return_value):
            error = SemanticError(
                f"{from_where}expects a type '{expected_return_value.name}', but '{expression_type}' was received, and it's not a subtype"
            )
            self.errors.append(error)
        return expression_type

    def check_argument_types[
        T
    ](
        self,
        argument_types: list[TypeInfo],
        original_arguments_defs: list[VarDefNode],
        from_where: str,
        caller_name: str = "function",
    ):
        """Checks if the types of the expressions that will be passed as arguments to a function (or method, type constructor, etc)
        are valid. It also modifies the AST node to give the correct type according to the inference process
        """
        if len(argument_types) != len(original_arguments_defs):
            error = SemanticError(
                f"{from_where}the {caller_name} expects {len(original_arguments_defs)} arguments, but {len(argument_types)} where given"
            )
            self.errors.append(error)
        for arg_type, original_arg in zip(argument_types, original_arguments_defs):
            expected_type = self.global_scope.get_type(original_arg.var_type)
            if isinstance(expected_type, NoneType):
                original_arg.var_type = arg_type.name
            elif not arg_type.conforms_to(expected_type):
                error = SemanticError(
                    f"{from_where}the argument with name {original_arg.var_name} expects a type {expected_type.name}, but {arg_type} was received"
                )
                self.errors.append(error)

    @visitor.on("node")
    def visit(
        self,
        node: AstNode,
        scope: HulkScopeLinkedNode,
        from_where: str = "",
    ) -> TypeInfo:
        """This is the main method of the class. It will execute the type inference of the node"""
        pass

    @visitor.when(ProgramNode)
    def visit(
        self,
        node: ProgramNode,
        scope: HulkScopeLinkedNode,
        from_where: str = "In the program file, ",
    ) -> TypeInfo:
        for declaration in node.declarations:
            self.visit(declaration, self.global_scope, from_where)
        self.visit(node.expr, self.global_scope, from_where)

    # region Basic Types to infer. This are the leafs of the tree

    @visitor.when(LiteralExpressionNode)
    def visit(
        self,
        node: LiteralExpressionNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ) -> TypeInfo:
        """This is a leaf node. It has a type that is the same as the literal"""
        if isinstance(node, LiteralNumNode) or isinstance(node, ConstantNode):
            return NumType()
        elif isinstance(node, LiteralBoolNode):
            return BoolType()
        # everything else will be taken as a string
        return StringType()

    @visitor.when(VarNode)
    def visit(
        self,
        node: VarNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ) -> TypeInfo:
        """This node represents the call of a variable in the scope to get it's value"""
        from_where += f"when calling the variable {node.value}, "
        if not scope.is_var_defined(node.value):
            error = SemanticError(
                f"{from_where}the variable {node.value} is not defined in the scope"
            )
            self.errors.append(error)
            return ErrorType()
        variable: VariableInfo = scope.get_variable(node.value)
        return scope.get_type(
            variable.type
        )  # TODO: Check if there is possible that this returns an error

    # endregion

    # region Node Operators

    @visitor.when(NegativeNode)
    def visit(
        self, node: NegativeNode, scope: HulkScopeLinkedNode, from_where: str
    ) -> TypeInfo:
        """This node represents the negative prefix operator. It will return a number"""
        from_where += "when calling the negative operator, "
        type_info = self.visit(node.value, scope, from_where)
        expected_type: TypeInfo = NumType()
        if not type_info.conforms_to(NumType()):
            error = SemanticError(
                f"{from_where}the expression must have type {expected_type.name} but it is of type '{type_info.name}'"
            )
            self.errors.append(error)
            return ErrorType()

        return expected_type

    @visitor.when(NotNode)
    def visit(
        self,
        node: NotNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ) -> TypeInfo:
        """This node represents the not operator. It will return a boolean"""
        from_where += "when calling the not operator, "
        type_info = self.visit(node.value, scope, from_where)
        expected_type: TypeInfo = BoolType()
        if not type_info.conforms_to(expected_type):
            error = SemanticError(
                f"{from_where}the expression must have type {expected_type.name} but it is of type '{type_info.name}'"
            )
            self.errors.append(error)
            return ErrorType()

        return expected_type

    @visitor.when(BinaryStringExpressionNode)
    def visit(
        self,
        node: BinaryExpressionNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ) -> TypeInfo:
        """This node represents the concatenation operator. It will return a string if everything is ok"""
        from_where += "when calling the concatenation operator, "
        left_type = self.visit(node.left, scope, from_where)
        right_type = self.visit(node.right, scope, from_where)
        expected_type: TypeInfo = StringType()
        return_type: TypeInfo = expected_type
        if not left_type.conforms_to(expected_type):
            error = SemanticError(
                f"{from_where}the expressions on the left side must have type {expected_type.name} but is of type '{left_type.name}'"
            )
            self.errors.append(error)
            return_type = ErrorType()
        if not right_type.conforms_to(expected_type):
            error = SemanticError(
                f"{from_where}the expressions on the right side must have type {expected_type.name} but is of type '{right_type.name}'"
            )
            self.errors.append(error)
            return_type = ErrorType()

        return return_type

    @visitor.when(BinaryNumExpressionNode)
    def visit(
        self, node: BinaryNumExpressionNode, scope: HulkScopeLinkedNode, from_where: str
    ) -> TypeInfo:
        """This node represents the binary operators for numbers. It will return a number if both of its side expressions are of type Number"""
        # from_where += "when calling the binary operator, "
        if isinstance(node, PlusNode):
            from_where += "when calling the plus operator, "
        elif isinstance(node, MinusNode):
            from_where += "when calling the minus operator, "
        elif isinstance(node, StarNode):
            from_where += "when calling the multiplication operator, "
        elif isinstance(node, DivNode):
            from_where += "when calling the division operator, "
        elif isinstance(node, ModNode):
            from_where += "when calling the division rest operator, "
        elif isinstance(node, PowNode):
            from_where += "when calling the power operator, "
        left_type = self.visit(node.left, scope, from_where)
        right_type = self.visit(node.right, scope, from_where)
        expected_type: TypeInfo = NumType()
        return_type = expected_type
        if not left_type.conforms_to(expected_type):
            error = SemanticError(
                f"{from_where}the expression on the left side must have type {expected_type.name} but is of type '{left_type.name}'"
            )
            self.errors.append(error)
            return_type = ErrorType()
        if not right_type.conforms_to(expected_type):
            error = SemanticError(
                f"{from_where}the expression on the right side must have type {expected_type.name} but is of type '{right_type.name}'"
            )
            self.errors.append(error)
            return_type = ErrorType()
        return return_type

    @visitor.when(BinaryBoolExpressionNode)
    def visit(
        self,
        node: BinaryBoolExpressionNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ) -> TypeInfo:
        """This node represents the binary operators for booleans. It will return a boolean if both of its side expressions are of type Boolean"""
        # from_where += "when calling the binary operator, "
        if isinstance(node, AndNode):
            from_where += "when calling the and operator, "
        elif isinstance(node, OrNode):
            from_where += "when calling the or operator, "
        elif isinstance(node, EqualNode):
            from_where += "when calling the equality operator, "
        elif isinstance(node, NotEqualNode):
            from_where += "when calling the inequality operator, "
        elif isinstance(node, LessNode):
            from_where += "when calling the less than operator, "
        elif isinstance(node, GreaterNode):
            from_where += "when calling the greater than operator, "
        elif isinstance(node, LeqNode):
            from_where += "when calling the less equal operator, "
        elif isinstance(node, GeqNode):
            from_where += "when calling the greater equal operator, "
        left_type = self.visit(node.left, scope, from_where)
        right_type = self.visit(node.right, scope, from_where)
        expected_type: TypeInfo = BoolType()
        return_type: TypeInfo = expected_type
        if not left_type.conforms_to(expected_type):
            error = SemanticError(
                f"{from_where}the expression on the left side must be of type '{expected_type.name}' but is of type '{left_type.name}'"
            )
            self.errors.append(error)
            return_type = ErrorType()
        if not right_type.conforms_to(expected_type):
            error = SemanticError(
                f"{from_where}the expression on the right side must be of type '{expected_type.name}' but is of type '{right_type.name}'"
            )
            self.errors.append(error)
            return_type = ErrorType()
        return return_type

    @visitor.when(DynTestNode)
    def visit(
        self,
        node: DynTestNode,
        scope: HulkScopeLinkedNode,
        from_where: str,
    ) -> TypeInfo:
        """This node represents the dynamic test operator. It will return a boolean"""
        from_where += "when calling the dynamic test operator, "
        expression_type: TypeInfo = self.visit(node.expr, scope, from_where)
        expected_type: TypeInfo = scope.get_type(node.type)
        if not expression_type.conforms_to(expected_type):
            error = SemanticError(
                f"{from_where}the right side type must conform to the left side type"
            )
            self.errors.append(error)
            return ErrorType()
        return BoolType()

    # endregion

    # region Calling Expressions

    @visitor.when(AttrCallNode)
    def visit(
        self, node: AttrCallNode, scope: HulkScopeLinkedNode, from_where: str
    ) -> TypeInfo:
        """This node represents the call of an attribute of an object. Only in the 'self' instance"""
        from_where += f"when calling the attribute with name '{node.variable_id}', "
        object_reference: VariableInfo = scope.get_variable("self")
        object_type: TypeInfo = scope.get_type(object_reference.type)
        if not object_type.is_attribute_defined(node.variable_id):
            error = SemanticError(
                f"{from_where}the attribute {node.variable_id} is not defined in the object of type '{object_type.name}'"
            )
            self.errors.append(error)
            return ErrorType()
        object_attribute: VariableInfo = object_type.get_attribute(node.variable_id)
        return scope.get_type(object_attribute.type)

    @visitor.when(FunctionCallNode)
    def visit(
        self, node: FunctionCallNode, scope: HulkScopeLinkedNode, from_where: str
    ) -> TypeInfo:
        """This node represents the call of a function. It will return the return type of the function"""
        from_where += f"when calling the function '{node.function_id}', "
        if not scope.is_function_defined(node.function_id):
            error = SemanticError(
                f"{from_where}the function {node.function_id} is not defined in the scope"
            )
            self.errors.append(error)
            return ErrorType()
        function: FunctionInfo = scope.get_function(node.function_id)
        # FIXME: Handle the case where the function_pointer is None, because is a builtin function
        # function_def_node: FunctionDeclarationNode = function.function_pointer
        # arguments = []
        if isinstance(function, BuiltinFunction):
            pass
        # Check the argument types
        expression_args: list[ExpressionNode] = node.arguments
        argument_types: list[TypeInfo] = []
        for index, expression in enumerate(expression_args):
            from_where_index = from_where + f"in the argument number {index}, "
            exp_type = self.visit(expression, scope, from_where_index)
            argument_types.append(exp_type)

        # Check the argument types and modify the AST
        # self.check_argument_types(
        #     argument_types,
        #     function_def_node.arguments,  # FIXME: This could be None because, the function could be a Builtin Function, and this functions have no declaration pointer
        #     from_where,
        #     "function",
        # )

        # TODO: Change this to return a type from the scope NOT A STRING
        return function.return_type


# endregion
