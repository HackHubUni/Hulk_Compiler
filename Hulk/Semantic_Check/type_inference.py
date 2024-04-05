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
    def visit(self, node: AstNode, scope: HulkScopeLinkedNode):
        """This is the main method of the class. It will execute the type inference of the node"""
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: HulkScopeLinkedNode):
        for declaration in node.declarations:
            self.visit(declaration, self.global_scope)
        self.visit(node.expr, self.global_scope)

    # region Basic Types to infer. This are the leafs of the tree

    @visitor.when(LiteralExpressionNode)
    def visit(self, node: LiteralExpressionNode, scope: HulkScopeLinkedNode):
        """This is a leaf node. It has a type that is the same as the literal"""
        node.type = node.literal_type


# endregion
