import cmp.visitor as visitor
from cmp.semantic import Scope
from Hulk.tools.Ast import *
from Hulk.Semantic_Check.checker import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.check_type_semantic import *
from Hulk.Semantic_Check.type_node import *



class TypeInferer:
    def __init__(self, context, errors = []) -> None:
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors


    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope=None):
        scope = Scope()
        for declaration in node.decl_list:
            self.visit(declaration, scope.create_child())
        self.visit(node.expr,scope.create_child())   
        self.inferred_type = node.expr.inferred_type
        return scope
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode, scope):
        for expression in node.expr_list:
            self.visit(expression, scope.create_child())
            self.inferred_type = expression.inferred_type

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope):
        for assign in node.assign_list:
            self.visit(assign,scope)
        self.visit(node.expr,scope.create_child())
        self.inferred_type = node.expr.inferred_type

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope):
        node.cond.inferred_type = BoolType()
        self.visit(node.if_expr,scope.create_child())
        branches_types = [node.if_expr.inferred_type]
        for elif_cond, elif_expr in node.elif_branches:
            elif_cond.inferred_type = BoolType()
            self.visit(elif_expr,scope.create_child())
            branches_types.append(elif_expr.inferred_type)
        self.visit(node.else_expr,scope.create_child())
        branches_types.append(node.else_expr.inferred_type)
        self.inferred_type = TypeInferer.lowest_common_ancestor()

    @staticmethod
    def lowest_common_ancestor(types: list[Type]):
       pass # ancester
        

    

