import cmp.visitor as visitor
from abc import ABC, abstractmethod
class Node:


    def evaluate(self):
        raise NotImplementedError()

class StringExpression:
    pass


class ConstantStringNode:
    pass


class TypeDeclarationNode:
    pass


class FuncDeclarationNode:
    pass


class ProtocolDeclarationNode:
    pass


class MethodDeclaration:
    pass


class FuncCallNode:
    pass


class AttrDeclarationNode:
    pass


class InstantiateNode:
    pass


class AttrCallNode:
    pass


class VoidNode:
    pass


class DestructiveAssignment:
    pass


class ConditionalNode:
    pass


class ElseBlockNode:
    pass


class LoopNode:
    pass


class ForNode:
    pass


class RangeNode:
    pass


class List_Comprehension:
    pass


class IndexationNode:
    pass


class ModNode:
    pass


class ConstantNumNode:
    pass


class ConstantBoolNode:
    pass


class ConformsNode:
    pass


class IsNode:
    pass


class NotNode:
    pass


class LeqNode:
    pass


class ExponEulerNode:
    pass


class SinNode:
    pass


class VariableNode:
    pass


class NegNode:
    pass


class EqualNode:
    pass


class PowNode:
    pass


class CosNode:
    pass


class LogNode:
    pass


class RandNode:
    pass


class LessNode:
    pass


class SqrtNode:
    pass


class AndNode:
    pass


class OrNode:
    pass

"""
class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements


class ParameterNode(Node):
    pass

class ClassAtributeNode(Node):
    pass

class ProtocolMethodNode(Node):
    pass

class StatementNode(Node):
    pass


class ExpressionNode(StatementNode):
    pass

class TypeNode(StatementNode):
    pass


class ProtocolNode(StatementNode):
    pass

class ExpressionNode(StatementNode):
    pass


class  ExpressionBlockNode(ExpressionNode):
    pass
class SimpleExpressionNode(ExpressionNode):
    pass

## Menor priopridad

class LetNode(SimpleExpressionNode):
    pass

class IfElseExpression(SimpleExpressionNode):
    pass

class DestructiveExpression(SimpleExpressionNode):
    pass

class whileNode(SimpleExpressionNode):
    pass

class forNode(SimpleExpressionNode):
    pass

class newNode(SimpleExpressionNode):
    pass

#Operaciones

class OrAndExpression(SimpleExpressionNode):
    pass

class NotExpression(SimpleExpressionNode):
    pass

class ComparationExpression(SimpleExpressionNode):
    pass

class IsExpression(SimpleExpressionNode):
    pass

class StringConcatenationNode(SimpleExpressionNode):
    pass

class AritmethicExpression(SimpleExpressionNode):
    pass

##Prioridad alta

class NumberNode(SimpleExpressionNode):
    pass

class StringNode(SimpleExpressionNode):
    pass

class BooleanNode(SimpleExpressionNode):
    pass

class Variable(SimpleExpressionNode):
    pass

class FunctionCallNode(SimpleExpressionNode):
    pass

class ClassAtributeCallNode(SimpleExpressionNode):
    pass

class ClassFunctionCallNode(SimpleExpressionNode):
    pass

class ListNode(SimpleExpressionNode):
    pass

class ImplicitListNode(SimpleExpressionNode):
    pass

class InexingNode(SimpleExpressionNode):
    pass

class asNode(SimpleExpressionNode):
    pass
    
"""