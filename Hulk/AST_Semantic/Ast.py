import cmp.visitor as visitor
from abc import ABC, abstractmethod
class Node:


    def evaluate(self):
        raise NotImplementedError()
    



class ProgramNode(Node):
    def __init__(self, statement_list,exp):
        self.exp = exp
        self.statements_list = statement_list

class StringExpression(Node):
    def __init__(self,string_type, concatenable):
        self.string_type = string_type
        self.concatenable = concatenable# expresion o string a concatenar

class ConstantStringNode(StringExpression):#tienen el string 
    def __init__(self, string_lex):
        super().__init__(string_lex, concatenable = None)




class TypeDeclarationNode(Node):
    def __init__(self, idx, type_body , a, type_args):
        


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

class LetNode:
    pass

