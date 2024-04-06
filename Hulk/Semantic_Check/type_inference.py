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
        return LiteralStrNode()

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
        return scope.get_variable(node.value).type

    # endregion

    # region Node Operators

    @visitor.when(NegativeNode)
    def visit(
        self, node: NegativeNode, scope: HulkScopeLinkedNode, from_where: str
    ) -> TypeInfo:
        """This node represents the negative prefix operator. It will return a number"""
        from_where += "when calling the negative operator, "
        type_info = self.visit(node.value, scope, from_where)
        if not isinstance(type_info, NumType):
            error = SemanticError(
                f"{from_where}the expression must have type {NumType.static_name()} but it is of type {type_info.name}"
            )
            self.errors.append(error)
            return ErrorType()


# endregion
