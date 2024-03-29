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
    def __init__(self, idx, type_body , idx_inherits, type_args):
        self.idx = idx
        self.type_body = type_body
        self.idx_inherits = idx_inherits
        self.type_args = type_args

class FuncDeclarationNode:
    def __init__(self,idx,param_list , exp ) -> None:
        self.idx = idx
        self.param_list = param_list
        self.exp = exp


class AttrDeclarationNode:# a=b a:b
    def __init__(self,idx,exp, type_exp):
        self.idx = idx
        self.type_exp = type_exp
        self.exp = exp


class InstantiateNode(Node):#new
    def __init__(self,idx,exp_list):
        def __init__(self,idx,exp_list):
            self.idx = idx
            self.exp_list = exp_list


#nodos de llamada
class CallNode(Node):
    def __init__(self,idx,exp_list):
        self.idx = idx
        self.exp_list = exp_list
class AttrCallNode(CallNode):
    def __init__(self,idx,exp):
        super().__init__(idx,exp)
        self.idx = idx
        self.exp = exp

class FuncCallNode(CallNode):
   def __init__(self,idx,exp_list):
        super().__init__(idx,exp_list)
        self.idx = idx
        self.exp_list = exp_list


class VoidNode(CallNode):#epsilon
    def __init__(self):
        super().__init__(None,None)
        self.value = None

#nodos de expresion
class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node



#nodos de condicionales

class LetNode(BinaryNode):
    def __init__(self, let_exp, in_exp):
        super().__init__(let_exp, in_exp)
        self.let_exp = let_exp
        self.in_exp = in_exp

class AssignNode(BinaryNode):#a =b
    def __init__(self, idx, value):
        super().__init__(idx, value)
        self.idx = idx
        self.value = value
    
class DestructiveAssignment(AssignNode):#a:=b
    def __init__(self, idx, value):
        super().__init__(idx, value)
        self.idx = idx
        self.value = value
                
class ConditionalNode(Node):
    def __init__(self, if_exp, if_body, else_body):
        self.if_exp = if_exp
        self.if_body = if_body
        self.else_body = else_body

class ElseBlockNode(UnaryNode):
    def __init__(self, else_body):
        super().__init__(else_body)
        self.else_body = else_body

class LoopNode(ConditionalNode):
    def __init__(self, if_exp, if_body, else_body):
        super().__init__(if_exp, if_body, else_body)
        self.while_exp = if_exp
        self.while_body = if_body
        self.else_body = else_body


class ForNode(Node):
    def __init__(self,  range_exp, for_body,idx,for_else_body):
        self.idx = idx
        self.range_exp = range_exp
        self.for_body = for_body
        self.for_else_body = for_else_body

#iterables
class RangeNode(BinaryNode):
    def __init__(self, start, end):
        super().__init__(start, end)
        self.start = start
        self.end = end

class List_Comprehension(Node):
    def __init__(self, exp, for_exp, if_exp):
        self.exp = exp
        self.for_exp = for_exp
        self.if_exp = if_exp

class IndexationNode(BinaryNode):
    def __init__(self, idx, exp):
        self.idx = idx
        self.exp = exp

#operaciones binarias
class ModNode(BinaryNode):  
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right


class PlusNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class MinusNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class StarNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class DivNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right  

class PowNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right


# unarios
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class VariableNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex
    
class ConstantNumNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

class NegNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

class sqrtNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

class CosNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

class SinNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

class ExponEulerNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

class LogNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

class RandNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

#condition

class EqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class LessNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class LeqNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class AndNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class OrNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right


class ConformsNode(BinaryNode): 
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class IsNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

class ConstantBoolNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.lex = lex

class NotNode(AtomicNode):
    def __init__(self, right):
        super().__init__(right)
        self.right = right


