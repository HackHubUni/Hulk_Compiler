import cmp.visitor as visitor
from abc import ABC, abstractmethod
from cmp.ast import *

class ProgramNode(Node):
    def __init__(self, decl_list, expr):
        self.decl_list:list[DeclarationNode] = decl_list
        self.expr = expr


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class ExpressionBlockNode(ExpressionNode):
    def __init__(self, expr_list:list) -> None:
        """
        Recibe  una lista de estamentos
        """
        self.expr_list = expr_list


class LetNode(ExpressionNode):
    def __init__(self, assign_list, expr) -> None:
        self.assign_list = assign_list
        self.expr = expr


class IfNode(ExpressionNode):
    def __init__(self, cond, if_expr, elif_branches, else_expr) -> None:
        self.cond = cond
        self.if_expr = if_expr
        self.elif_branches = elif_branches  # lista de tuplas de expresiones del tipo (elif_cond, elif_expr)
        self.else_expr = else_expr


class WhileNode(ExpressionNode):
    def __init__(self, cond, body) -> None:
        self.cond = cond
        self.body = body


class ForNode(ExpressionNode):
    def __init__(self, id, iterable, body) -> None:
        self.id = id
        self.iterable = iterable
        self.body = body


class DestrAssign(ExpressionNode):
    def __init__(self, id, expr, is_attr=False) -> None:
        self.id = id
        self.expr = expr
        self.is_attr = is_attr


class AssignNode(Node):
    def __init__(self, var, expr) -> None:
        self.var = var
        self.expr = expr


class VarDefNode(Node):
    def __init__(self, id, type=None) -> None:
        self.id = id
        self.type = type


class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return str(lvalue) + str(rvalue)


class ConcatWithSpaceNode(BinaryNode):
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


class DynTestNode(ExpressionNode):
    def __init__(self, expr, type) -> None:
        self.expr = expr
        self.type = type


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
    pass


class LiteralBoolNode(AtomicNode):
    pass


class LiteralStrNode(AtomicNode):
    pass


class ConstantNode(AtomicNode):
    pass


class VarNode(AtomicNode):
    pass


class VectorNode(ExpressionNode):
    def __init__(self, expr_list) -> None:
        self.expr_list = expr_list


class ImplicitVector(ExpressionNode):
    def __init__(self, expr, id, iterable) -> None:
        self.expr = expr
        self.id = id
        self.iterable = iterable


class IndexingNode(ExpressionNode):
    def __init__(self, vector, index):
        self.vector = vector
        self.expr = index


class InstantiateNode(ExpressionNode):
    def __init__(self, type, expr_list) -> None:
        self.type = type
        self.expr_list = expr_list


class DowncastNode(ExpressionNode):
    def __init__(self, obj, type) -> None:
        self.obj = obj
        self.type = type


class FuncCallNode(ExpressionNode):
    def __init__(self, id, args):
        self.id = id
        self.args = args


class MethodCallNode(ExpressionNode):
    def __init__(self, obj, id, args):
        self.obj = obj
        self.id = id
        self.args = args


class AttrrCallNode(ExpressionNode):
    def __init__(self, obj, id) -> None:
        self.obj = obj
        self.id = id


class FunctionDeclarationNode(DeclarationNode):
    def __init__(self, id, args, body, return_type=None) -> None:
        self.id = id
        self.args = args
        self.return_type = return_type
        self.body = body

class BuiltinFunction(FunctionDeclarationNode):
    def evaluate(self):
        pass
    

class SinBuiltingFunction(BuiltinFunction):
    def __init__(self) -> None:
        super().__init__()
        self.id = 'sin'
        self.args = [VarDefNode('x','Num')]
        self.return_type = 'Num'
    
class CosBuiltingFunction(BuiltinFunction):
    def __init__(self, id, args, body, return_type=None) -> None:
        super().__init__()
        self.id = 'cos'
        self.args = [VarDefNode('x', 'Num')]
        self.return_type = 'Num'


class TypeDeclarationNode(DeclarationNode):
    def __init__(self, id, features, args=None, parent=None, parent_constructor_args=None) -> None:
        self.id = id
        self.features = features
        self.args = args
        self.parent = parent
        self.parent_constructor_args = parent_constructor_args


class MethodNode(Node):
    def __init__(self, id, args, body, return_type=None) -> None:
        self.id = id
        self.args = args
        self.return_type = return_type
        self.body = body


class ProtDeclarationNode(DeclarationNode):
    def __init__(self, id, methods, parents=None) -> None:
        self.id = id
        self.methods = methods
        self.parents = parents


class PrototypeMethodNode(Node):
    def __init__(self, id, args: list[VarDefNode], return_type) -> None:
        self.id = id
        self.args = args
        self.return_type = return_type