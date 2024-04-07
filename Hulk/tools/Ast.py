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


class ExpressionBlockNode(ExpressionNode):
    """"""
    def __init__(
        self,
        expr_list: list,
    ):
        """
        Recibe una lista de statements
        """
        self.expr_list: list = expr_list


class UnaryExpressionNode(ExpressionNode):
    def __init__(self, value: ExpressionNode) -> None:
        self.value: ExpressionNode = value


class LiteralExpressionNode(UnaryExpressionNode):
    """This node groups all the literal nodes"""

    pass


class BinaryExpressionNode(ExpressionNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode):
        self.left: ExpressionNode = left
        self.right: ExpressionNode = right


# region Atomic Units of the Language  ----->   Literals and ¿VarNode?
class LiteralNumNode(LiteralExpressionNode):
    pass


class LiteralBoolNode(LiteralExpressionNode):
    pass


class LiteralStrNode(LiteralExpressionNode):
    pass


class ConstantNode(LiteralExpressionNode):
    pass


class VarNode(UnaryExpressionNode):
    """This node have a single element and this is the identifier of the variable to which extract the value"""

    pass


# endregion

# region Operators


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

# endregion


# region Calling Expressions
class AttrCallNode(ExpressionNode):
    """This node represents the intent of accessing a variable in the 'self' instance"""

    def __init__(
        self,
        variable_id: str,
    ):
        self.variable_id: str = variable_id
        """This is the variable that you want to access in the self instance"""


class FunctionCallNode(ExpressionNode):
    def __init__(
        self,
        id: str,
        args: list[ExpressionNode],
    ):
        self.id: str = id
        self.args: list[ExpressionNode] = args


class MethodCallNode(ExpressionNode):
    def __init__(self,
        method_id: str,
                 args):
        self.method_id: str = method_id
        """The identifier of the method"""
        self.args = args
        """The arguments of the method"""


class MethodCallWithExpressionNode(MethodCallNode):
    """This is a Node that has an expression to evaluate and to execute this method on the result of the expression"""

    def __init__(
        self,
        object_expression: ExpressionNode,
        method_id: str,
        args,
    ):
        super().__init__(method_id, args)
        self.object_expression: ExpressionNode = object_expression
        """This is an expression that when evaluated should return a type to which to ask to execute the method"""



class MethodCallWithIdentifierNode(MethodCallNode):
    def __init__(
        self,
        object_id: str,
        method_id: str,
        args,
    ):
        super().__init__(method_id, args)
        self.object_id: str = object_id



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


# endregion

# region Variable Related Nodes


class VarDefNode(AstNode):
    def __init__(
        self,
        id: str,
        type: str = None,
    ):
        self.id: str = id
        self.type: str = type


class AssignNode(ExpressionNode):
    def __init__(
        self,
        var: VarDefNode,
        expr,
    ):
        self.var: VarDefNode = var
        self.expr = expr


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
    """
    Destruir el valor del atributo que contengo yo
    """
    def __init__(
        self,
        attribute_call_expression: AttrCallNode,
        expression: ExpressionNode,
    ):
        self.attribute_call_expression: AttrCallNode = attribute_call_expression
        """This is a pointer to the AttributeCallNode that when evaluated """
        self.expression: ExpressionNode = expression
        """This is the expression whose value must go in the value of the Variable Info returned by the attribute_call_expression"""


# endregion


# region Conditional Related Expressions
class ElifNodeAtomExpression(ExpressionNode):
    def __init__(
        self,
        conditional_expression: ExpressionNode,
        body_expression: ExpressionNode,
    ):
        self.conditional_expression: ExpressionNode = conditional_expression
        """This is the expression that MUST evaluate True"""
        self.body_expression: ExpressionNode = body_expression
        """This is the body of the ElifNodeAtom this branch should execute if the condition is true"""


class ElifNodeExpressionList(ExpressionNode):
    def __init__(self, elif_expressions: list[ElifNodeAtomExpression]):
        self.elif_expressions: list[ElifNodeAtomExpression] = elif_expressions
        """This value could be empty"""


class IfNodeExpression(ExpressionNode):
    def __init__(
        self,
        conditional_expression: ExpressionNode,
        if_body_expression: ExpressionNode,
        elif_branches: ElifNodeExpressionList,
        else_expression: ExpressionNode,
    ):
        self.conditional_expression: ExpressionNode = conditional_expression
        """This is the expression inside the parenthesis of the If expression. It must be a bool"""
        self.if_body_expression: ExpressionNode = if_body_expression
        """This is the body that should get executed if the conditional expression is True"""
        self.elif_branches: ElifNodeExpressionList = elif_branches
        """This is a Node that contains a List of ElifNodeAtom"""
        self.else_expression: ExpressionNode = else_expression
        """This is the expression that will be executed in the Else branch"""


# endregion


# region Loop Related Expressions
class WhileExpressionNode(ExpressionNode):
    def __init__(
        self,
        conditional_expression: ExpressionNode,
        body_expression: ExpressionNode,
    ):
        self.conditional_expression: ExpressionNode = conditional_expression
        self.body_expression: ExpressionNode = body_expression


class ForExpressionNode(ExpressionNode):
    def __init__(
        self,
        id: str,
        iterable: ExpressionNode,
        body: ExpressionNode,
    ):
    #TODO: Write for node as While expression

        self.id: str = id
        """This is the name of the identifier that will store the value of the current element of the iterable"""
        self.iterable: ExpressionNode = iterable
        """This is an Expression that Must evaluate to a Type that implements the Iterable Protocol"""
        self.body: ExpressionNode = body
        """This is the body of the For. The code that must be evaluated in each cicle of the iterable"""


# endregion


# region Nodes related with Vectors
class VectorNode(ExpressionNode):
    """This node represents the creation of a vector"""

    def __init__(
        self,
        expression_list: list[ExpressionNode],
    ):
        self.expression_list: list[ExpressionNode] = expression_list


class ImplicitVector(ExpressionNode):
    """Represents the creation of a vector in its implicit form"""

    def __init__(
        self,
        expression_body: ExpressionNode,
        id: str,
        iterable: ExpressionNode,
    ):
        self.expression_body: ExpressionNode = expression_body
        """This expression represents the code that will be executed for each element of the Iterable"""
        self.id: str = id
        """The name of the variable that will represents the current value of the iterable"""
        self.iterable: ExpressionNode = iterable
        """This expression should evaluate to a type that implements the Iterable Protocol"""


class IndexingNode(ExpressionNode):
    def __init__(
        self,
        vector_expression: ExpressionNode,
        index: str,
    ):
        self.vector_expression: ExpressionNode = vector_expression
        """This is an expression that Must return a Vector Type"""
        self.index: str = index
        """This string Must be a number. But remember to cast it to INT"""


# endregion


# region Nodes related to Type Handling
class DowncastNode(ExpressionNode):
    """This is the expression for the code:\n
    x as Point\n
    Where Point is a Type"""

    def __init__(
        self,
        obj_expression: ExpressionNode,
        type: str,
    ):
        self.obj_expression: ExpressionNode = obj_expression
        self.type: str = type


class InstantiateNode(ExpressionNode):
    """This node creates a new instance of a type"""

    def __init__(
        self,
        type_id: str,
        initialization_expressions: list[ExpressionNode],
    ):
        self.type_id: str = type_id
        self.initialization_expressions: list[ExpressionNode] = (
            initialization_expressions
        )


# endregion


# region Nodes related with declarations
class LetNode(ExpressionNode):
    def __init__(
        self,
        assign_list: list[AssignNode],
        expr: ExpressionNode,
    ):
        self.assign_list: list[AssignNode] = assign_list
        """The list of all the Variables created in this let expression"""
        self.expr: ExpressionNode = expr
        """The Expression after the 'in'"""


class FunctionDeclarationNode(DeclarationNode):
    def __init__(
        self,
        id: str,
        args: list[VarDefNode],
        body: ExpressionNode,
        return_type: str = None,
    ):
        self.id: str = id
        """This is the name of the function"""
        self.args: list[VarDefNode] = args
        """This is the List of the Arguments of the Function"""
        self.return_type: str = return_type
        """This is the return Type"""
        self.body: ExpressionNode = body
        """This is the expression body of the Function"""


class MethodNode(DeclarationNode):  # MethodDeclarationNode
    """This is the Node for method Declarations inside Types"""

    def __init__(
        self,
        id: str,
        args: list[VarDefNode],
        body: ExpressionNode,
        return_type: str = None,
    ):
        self.id: str = id
        self.args: list[VarDefNode] = args
        self.return_type: str = return_type
        self.body: ExpressionNode = body


class TypeDeclarationNode(DeclarationNode):
    """This node represents the construction of a Type"""

    def __init__(
        self,
        id: str,
        features: list[AssignNode | MethodNode],
        args: list[VarDefNode] = [],
        parent: str = None,
        parent_constructor_args: list[ExpressionNode] = None,
    ):
        self.id: str = id
        self.features: list[AssignNode | MethodNode] = features
        self.args: list[VarDefNode] = args
        self.parent: str = parent
        """This is a string with the name of the parent type"""
        self.parent_constructor_args: list[ExpressionNode] = parent_constructor_args
        """This is a list of Expressions. Could be None"""


class ProtocolMethodNode(DeclarationNode):
    def __init__(
        self,
        id: str,
        args: list[VarDefNode],
        return_type: str,
    ):
        self.id: str = id
        self.args: list[VarDefNode] = args
        self.return_type: str = return_type


class ProtocolDeclarationNode(DeclarationNode):
    def __init__(
        self,
        id: str,
        methods: list[ProtocolMethodNode],
        parents: list[str] = None,
    ):
        self.id: str = id
        """This is the name of the Protocol"""
        self.methods: list[ProtocolMethodNode] = methods
        """A list with all the protocol methods"""
        self.parents: list[str] = parents
        """A list with all the protocol parents that this protocol extends"""


# endregion
