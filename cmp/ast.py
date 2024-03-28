import cmp.visitor as visitor
from abc import ABC, abstractmethod


class Node:


    def evaluate(self):
        raise NotImplementedError()


class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

    def __str__(self):
        return str(self.lex)


class UnaryNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()


class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()




#################
#Nuevos nodos ##
################
class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements


class ParameterNode(Node):
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