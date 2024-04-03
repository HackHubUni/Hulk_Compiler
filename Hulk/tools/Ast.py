import cmp.visitor as visitor
from abc import ABC, abstractmethod


class AstNode:
    """Base class for all nodes of the AST"""

    pass


class ProgramNode(AstNode):
    def __init__(self, decl_list, expr):
        self.decl_list: list[DeclarationNode] = decl_list
        self.expr = expr


class DeclarationNode(AstNode):
    pass


class ExpressionNode(AstNode):
    pass


class UnaryExpressionNode(ExpressionNode):
    def __init__(self, value: ExpressionNode) -> None:
        self.value: ExpressionNode = value


# region UnaryNumExpressions
class UnaryNumExpressionNode(UnaryExpressionNode):
    pass


class NegativeNode(UnaryNumExpressionNode):
    pass


# endregion


# region UnaryBoolExpressions
class UnaryBoolExpressionNode(UnaryExpressionNode):
    pass


class NotNode(UnaryBoolExpressionNode):
    pass


# endregion


class BinaryExpressionNode(ExpressionNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode):
        self.left: ExpressionNode = left
        self.right: ExpressionNode = right


# region BinaryStringExpressions
class BinaryStringExpressionNode(BinaryExpressionNode):
    """This node groups all binary operations over the String type"""

    pass


class ConcatNode(BinaryStringExpressionNode):
    pass


class ConcatWithSpaceNode(BinaryStringExpressionNode):
    pass


# endregion


# region BinaryNumExpressions
class BinaryNumExpressionNode(BinaryExpressionNode):
    """This node groups all binary operations over the Num type"""

    pass


class PlusNode(BinaryNumExpressionNode):
    pass


class MinusNode(BinaryNumExpressionNode):
    pass


class StarNode(BinaryNumExpressionNode):
    pass


class DivNode(BinaryNumExpressionNode):
    pass


class ModNode(BinaryNumExpressionNode):
    pass


class PowNode(BinaryNumExpressionNode):
    pass


# endregion


# region BinaryBoolExpressions
class BinaryBoolExpressionNode(BinaryExpressionNode):
    """This node groups all binary operations over the Bool type"""

    pass


class OrNode(BinaryBoolExpressionNode):
    pass


class AndNode(BinaryBoolExpressionNode):
    pass


class EqualNode(BinaryBoolExpressionNode):
    pass


class NotEqualNode(BinaryBoolExpressionNode):
    pass


class LessNode(BinaryBoolExpressionNode):
    pass


class GreaterNode(BinaryBoolExpressionNode):
    pass


class LeqNode(BinaryBoolExpressionNode):
    pass


class GeqNode(BinaryBoolExpressionNode):
    pass


# endregion


# region Another Bool Expression
class DynTestNode(ExpressionNode):  # This is for expression like --> Expression is Type
    def __init__(
        self,
        expr,
        type,
    ):
        self.expr = expr
        self.type = type


# endregion


class ExpressionBlockNode(ExpressionNode):
    def __init__(
        self,
        expr_list: list,
    ):
        """
        Recibe una lista de statements
        """
        self.expr_list: list = expr_list


class AttrCallNode(ExpressionNode):
    """This node represents the intent of accessing a variable in the 'self' instance"""

    def __init__(
        self,
        variable_id: str,
    ):
        self.variable_id: str = variable_id
        """This is the variable that you want to access in the self instance"""


class LetNode(ExpressionNode):
    def __init__(
        self,
        assign_list,
        expr,
    ):
        self.assign_list = assign_list
        self.expr = expr


class IfNode(ExpressionNode):
    def __init__(
        self,
        cond,
        if_expr,
        elif_branches,
        else_expr,
    ):
        self.cond = cond
        self.if_expr = if_expr
        self.elif_branches = elif_branches  # lista de tuplas de expresiones del tipo (elif_cond, elif_expr)
        self.else_expr = else_expr


class WhileNode(ExpressionNode):
    def __init__(
        self,
        cond,
        body,
    ):
        self.cond = cond
        self.body = body


class ForNode(ExpressionNode):
    def __init__(
        self,
        id,
        iterable,
        body,
    ):
        self.id = id
        self.iterable = iterable
        self.body = body


class DestructionAssignmentBasicExpression(ExpressionNode):
    def __init__(
        self,
        id: str,
        expr: ExpressionNode,
    ):
        self.id: str = id
        """This is the identifier of the variable to update it's value"""
        self.expr: ExpressionNode = expr
        """The result of this expression is the value that will update the previous one"""


class DestructionAssignmentWithAttributeCallExpression(ExpressionNode):
    def __init__(
        self,
        attribute_call_expression: AttrCallNode,
        expression: ExpressionNode,
    ):
        self.attribute_call_expression: AttrCallNode = attribute_call_expression
        """This is a pointer to the AttributeCallNode that when evaluated """
        self.expression: ExpressionNode = expression
        """This is the expression whose value must go in the value of the Variable Info returned by the attribute_call_expression"""


class VarDefNode(AstNode):
    def __init__(
        self,
        id: str,
        type: str = None,
    ):
        self.id: str = id
        self.type: str = type


class AssignNode(AstNode):
    def __init__(
        self,
        var: VarDefNode,
        expr,
    ):
        self.var: VarDefNode = var
        self.expr = expr


class LiteralNumNode(UnaryExpressionNode):
    pass


class LiteralBoolNode(UnaryExpressionNode):
    pass


class LiteralStrNode(UnaryExpressionNode):
    pass


class ConstantNode(UnaryExpressionNode):
    pass


class VarNode(UnaryExpressionNode):
    pass


class VectorNode(ExpressionNode):
    def __init__(
        self,
        expr_list,
    ):
        self.expr_list = expr_list


class ImplicitVector(ExpressionNode):
    def __init__(
        self,
        expr,
        id,
        iterable,
    ):
        self.expr = expr
        self.id = id
        self.iterable = iterable


class IndexingNode(ExpressionNode):
    def __init__(
        self,
        vector,
        index,
    ):
        self.vector = vector
        self.expr = index


class InstantiateNode(ExpressionNode):
    def __init__(
        self,
        type,
        expr_list,
    ):
        self.type = type
        self.expr_list = expr_list


class DowncastNode(ExpressionNode):
    def __init__(
        self,
        obj,
        type,
    ):
        self.obj = obj
        self.type = type


class FuncCallNode(ExpressionNode):
    def __init__(
        self,
        id: str,
        args: list[ExpressionNode],
    ):
        self.id: str = id
        self.args: list[ExpressionNode] = args


class MethodCallNode(ExpressionNode):
    pass


class MethodCallWithExpressionNode(MethodCallNode):
    """This is a Node that has an expression to evaluate and to execute this method on the result of the expression"""

    def __init__(
        self,
        object_expression: ExpressionNode,
        method_id: str,
        args,
    ):
        self.object_expression: ExpressionNode = object_expression
        """This is an expression that when evaluated should return a type to which to ask to execute the method"""
        self.method_id: str = method_id
        """The identifier of the method"""
        self.args = args
        """The arguments of the method"""


class MethodCallWithIdentifierNode(MethodCallNode):
    def __init__(
        self,
        object_id: str,
        method_id: str,
        args,
    ):
        self.object_id: str = object_id
        self.method_id: str = method_id
        self.args = args


class MethodCallListNode(ExpressionNode):
    """This Node represents a list of consecutive method calls.\n
    Example: lets say you have a variable x of type Triangle. This node represents a code line like:\n
    x.get_point(1).get_norm()\n
    Where ---> get_point(1) and get_norm() are two methods and the second one is executed over the type returned by the first method.\n
    Note for Semantic Check
    -------
    When you have a line code like:\n
    get_default_triangle().get_point(1).get_norm()\n
    The first element is a FuncCallNode that is supposed to return an object of type Triangle, and this object will be stored
    in a new scope as a variable under the name 'self' pointing to the instance of Triangle. This scope will be passed to
    the first MethodCallNode of this Node"""

    def __init__(
        self,
        methods: list[MethodCallNode],
    ):
        self.methods: list[MethodCallNode] = methods


class FunctionDeclarationNode(DeclarationNode):
    def __init__(
        self,
        id: str,
        args: list[VarDefNode],
        body,
        return_type: str = None,
    ):
        self.id: str = id
        self.args: list[VarDefNode] = args
        self.return_type: str = return_type
        self.body = body


class MethodNode(AstNode):  # MethodDeclarationNode
    """This is the Node for method Declarations"""

    def __init__(
        self,
        id,
        args,
        body,
        return_type=None,
    ):
        self.id = id
        self.args = args
        self.return_type = return_type
        self.body = body


class TypeDeclarationNode(DeclarationNode):
    """This node represents the construction of a Type"""

    def __init__(
        self,
        id: str,
        features: list[AssignNode | MethodNode],
        args: list[VarDefNode] = [],
        parent: str = None,
        parent_constructor_args=None,
    ):
        self.id: str = id
        self.features: list[AssignNode | MethodNode] = features
        self.args: list[VarDefNode] = args
        self.parent: str = parent
        """This is a string with the name of the parent"""
        self.parent_constructor_args = parent_constructor_args
        """This is a list of Expressions. Could be None"""


class PrototypeMethodNode(AstNode):
    def __init__(
        self,
        id: str,
        args: list[VarDefNode],
        return_type,
    ):
        self.id: str = id
        self.args = args
        self.return_type = return_type


class ProtDeclarationNode(DeclarationNode):
    def __init__(
        self,
        id: str,
        methods: list[PrototypeMethodNode],
        parents: list[str] = None,
    ):
        self.id: str = id
        self.methods = methods
        self.parents = parents
