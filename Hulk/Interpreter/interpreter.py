from Hulk.Semantic_Check.basic_types.scopes import *
from Hulk.Semantic_Check.check_semantics import check_semantics
from Hulk.Semantic_Check.basic_types.scopes import *


class Interpreter(object):
    def __init__(self, context:HulkScopeLinkedNode, errors=[]):
        self.context = context
        self.errors:list[str] = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):

        try:
            for expression in node.expressions:
                self.visit(expression)
        except SemanticError as e:
           self.errors.append(e)


    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode):
        try:
             pass
        except SemanticError as e:
           self.errors.append(e)


