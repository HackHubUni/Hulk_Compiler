import cmp.visitor as visitor
from abc import ABC, abstractmethod
from cmp.ast import *
from Hulk.Semantic_Check.type_node import *
from cmp.pycompiler import Terminal
class ExpressionNode(Node):
    pass

class AssignNode(Node):
    def __init__(self, var, expr) -> None:
        self.var = var
        self.expr = expr
class ProgramNode(Node):
    def __init__(self, decl_list:list, expr:ExpressionNode):
        self.decl_list = decl_list
        self.expr = expr


class DeclarationNode(Node):
    pass





class ExpressionBlockNode(ExpressionNode):
    def __init__(self, expr_list:list[ExpressionNode]) -> None:
        self.expr_list = expr_list


class LetNode(ExpressionNode):
    def __init__(self, assign_list:list[AssignNode], expr:ExpressionNode) -> None:
        self.assign_list = assign_list
        self.expr = expr


class IfNode(ExpressionNode):
    def __init__(self, cond:ExpressionNode, if_expr:ExpressionNode, elif_branches:list[ExpressionNode], else_expr:ExpressionNode) -> None:
        self.cond = cond
        self.if_expr = if_expr
        self.elif_branches = elif_branches  # lista de tuplas de expresiones del tipo (elif_cond, elif_expr)
        self.else_expr = else_expr


class WhileNode(ExpressionNode):
    def __init__(self, cond:ExpressionNode, body:ExpressionNode) -> None:
        self.cond = cond
        self.body = body


class ForNode(ExpressionNode):
    def __init__(self, id_:Terminal, iterable:ExpressionNode, body:ExpressionNode) -> None:
        self.id = id_
        self.iterable = iterable
        self.body = body


class DestrAssign(ExpressionNode):
    def __init__(self, id_:Terminal, expr:ExpressionNode, is_attr:bool=False) -> None:
        self.id = id_
        self.expr = expr
        self.is_attr = is_attr





class VarDefNode(Node):
    def __init__(self, id_:Terminal, type:Terminal=None) -> None:
        """
        id_ nombre de la variable a declarar
        type: tipado de la variable a tipar
        """
        self.id = id_
        self.type = type

class ConcatNodeBase(BinaryNode):
    pass
class ConcatNode(ConcatNodeBase):

    def __init__(self,arithmetic:ConcatNodeBase,concat_to:BinaryNode|ExpressionNode|Node):
        self.arithmetic=arithmetic
        self.concat_to=concat_to
    @staticmethod
    def operate(lvalue, rvalue):
        return str(lvalue) + str(rvalue)


class ConcatWithSpaceNode(ConcatNode):

    @staticmethod
    def operate(lvalue, rvalue):
        return str(lvalue) + " " + str(rvalue)


class OrNode(BinaryNode):

    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue or rvalue


class AndNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue and rvalue


class NotNode(UnaryNode):
    @staticmethod
    def operate(value):
        return not value




class EqualNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue == rvalue


class NotEqualNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue != rvalue


class LessNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue < rvalue


class GreaterNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue > rvalue


class LeqNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue <= rvalue


class GeqNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue >= rvalue


class PlusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue + rvalue


class MinusNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue - rvalue


class StarNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue * rvalue


class DivNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue / rvalue


class ModNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue % rvalue


class PowNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue ** rvalue


class NegativeNode(UnaryNode):
    @staticmethod
    def operate(value):
        return - value


class LiteralNumNode(AtomicNode):
    def __init__(self, lex):
        AtomicNode.__init__(self, lex)
        self.inferred_type = NumType()

class LiteralBoolNode(AtomicNode):
    def __init__(self, lex):
        AtomicNode.__init__(self, lex)
        self.inferred_type = BoolType()
class LiteralStrNode(AtomicNode):
    pass

class ConstantNode(AtomicNode):
    def __init__(self, lex):
        AtomicNode.__init__(self, lex)
        self.inferred_type = NumType()

class VarNode(AtomicNode):
    pass


class VectorNode(ExpressionNode):
    def __init__(self, expr_list:list) -> None:
        self.expr_list = expr_list


class ImplicitVector(ExpressionNode):
    def __init__(self, expr:ExpressionNode|Node, id_:Terminal, iterable:ExpressionNode|Node) -> None:
        self.expr = expr
        self.id = id_
        self.iterable = iterable


class IndexingNode(ExpressionNode):
    def __init__(self, vector:list|Node, index:ExpressionNode|Node):
        self.vector = vector
        self.expr = index


class InstantiateNode(ExpressionNode):
    def __init__(self, type:Terminal, expr_list:list) -> None:
        self.type = type
        self.expr_list = expr_list


class DowncastNode(ExpressionNode):
    def __init__(self, obj:list|Node, type:Terminal) -> None:
        self.obj = obj
        self.type = type


class FuncCallNode(ExpressionNode):
    def __init__(self, id_:Terminal, args:list):
        self.id = id_
        self.args = args


class MethodCallNode(ExpressionNode):
    def __init__(self, obj:Terminal, id_:Terminal, args:list):
        self.obj = obj
        self.id = id_
        self.args = args

class MethodsCallNode(MethodCallNode):
    def __init__(self, obj:Terminal, id_:Terminal, args:list,next_calls:list[MethodCallNode]):
        super().__init__(obj, id_, args)
        self.next_calls=next_calls #TODO: Osea en orden el resto de funciones que llama

class AttrrCallNode(ExpressionNode):
    def __init__(self, obj:Terminal, id_:Terminal) -> None:
        self.obj = obj
        self.id = id_


class FunctionDeclarationNode(DeclarationNode):
    def __init__(self, id_:Terminal, args:list, body:list|ExpressionNode|Node, return_type:Terminal=None) -> None:
        self.id = id_
        self.args = args
        self.return_type = return_type
        self.body = body


class TypeDeclarationNode(DeclarationNode):
    def __init__(self, id_:Terminal, features:list|Terminal, args=None, parent=None, parent_constructor_args=None) -> None:
        self.id = id_
        self.features = features
        self.args = args
        self.parent = parent
        self.parent_constructor_args = parent_constructor_args


class MethodNode(Node):
    def __init__(self, id_:Terminal, args:list, body:Node|list, return_type:Terminal=None) -> None:
        self.id = id_
        self.args = args
        self.return_type = return_type
        self.body = body
class PrototypeMethodNode(Node):
    def __init__(self, id, args: list[VarDefNode], return_type) -> None:
        self.id = id
        self.args = args
        self.return_type = return_type

class ProtDeclarationNode(DeclarationNode):
    def __init__(self, id_:Terminal, methods:list[ PrototypeMethodNode], parents=None) -> None:
        self.id = id_
        self.methods = methods
        self.parents = parents





class DynTestNode(ExpressionNode):
    def __init__(self, expr:Node|UnaryNode|AtomicNode|BinaryNode|VectorNode|ImplicitVector|InstantiateNode|FuncCallNode|DowncastNode|IndexingNode|MethodCallNode|AttrrCallNode, type:Terminal) -> None:
        """
        expr: La expresión a recibir que puede ser cualquiera de las anteriores
        type: id del type
        """

        self.expr = expr
        self.type = type
