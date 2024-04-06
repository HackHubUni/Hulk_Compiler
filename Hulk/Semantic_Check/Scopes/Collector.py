from Hulk.Semantic_Check.Scopes.Collector_Scope import Collector_Info, HulkScope
from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.Scopes.hulk_global_scope import HulkGlobalScope, TypeScope, MethodScope, FunctionScope


def parents_check(initial_type, parent):
    if parent is None:
        return
    this_type = parent.id
    if initial_type == this_type:
        return True
    if parent.father:
        return parents_check(initial_type, parent.father)
    else:
        return False


class Collector(object):
    """
    Recolecta toda la información relevante de los scopes del hulk
    """

    def __init__(self, errors=[]):
        self.context: Collector_Info =None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, local_scope=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, local_scope=None):
        try:
           self.context = Collector_Info()
           # LLamar a cada declariacion del metodo
           for class_declaration in node.decl_list:
               self.visit(class_declaration, self.context)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_function_declaration(node)

            for features in node.args:
                self.visit(features, scope)
            self.visit(node.body, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)


    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_function_call(node,local_scope)

            for features in node.args:
                self.visit(features, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)


    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode, local_scope:Collector_Info):
        try:
            scope=   local_scope.add_protocol(node)
            for method in node.methods:
                self.visit(method, scope)

        except SemanticError as ex:
            self.errors.append(ex.text)


    @visitor.when(ProtocolMethodNode)
    def visit(self, node: ProtocolMethodNode, local_scope:HulkScope):
        # El scope que viene es el del padre hay que crear uno nuevo
        try:
            scope=  self.context.add_procols_methods(node, local_scope)
            for features in node.args:
                self.visit(features, scope)

        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode, local_scope: Collector_Info):
        try:
            scope = local_scope.add_type(node)
            for features in node.features:
                self.visit(features, scope)



        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodNode)
    def visit(self, node:MethodNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_type_methods(node,local_scope)
            for features in node.args:
                self.visit(features, scope)

                self.visit(node.body, scope)



        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(AttrCallNode)
    def visit(self, node: AttrCallNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_call_attr(node, local_scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_call_methods(node, local_scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodCallListNode)
    def visit(self, node: MethodCallListNode, local_scope: Collector_Info):
        try:

            for method in node.methods:
                self.visit(method, local_scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_assign(node, local_scope)

            #Visitar la variable
            self.visit(node.var, scope)
            #visitar la expression
            self.visit(node.expr, scope)


        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(VarDefNode)
    def visit(self, node:VarDefNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_var_def(node, local_scope)
        except SemanticError as ex:
            self.errors.append(ex.text)


    @visitor.when(DestructionAssignmentWithAttributeCallExpression)
    def visit(self, node: DestructionAssignmentWithAttributeCallExpression, local_scope: Collector_Info):
        try:

            scope = self.context.add_destruction_assignment_with_attribute_call(node, local_scope)
            #Visitar el attr call
            self.visit(node.attribute_call_expression, scope)
            #Visitar la expresion
            self.visit(node.expression, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(DestructionAssignmentBasicExpression)
    def visit(self, node: DestructionAssignmentBasicExpression, local_scope: Collector_Info):
        try:
            scope = self.context.add_destruction_assignment_basic(node, local_scope)
            self.visit(node.expression, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(BinaryExpressionNode)
    def visit(self, node: BinaryExpressionNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_binary_expression(node, local_scope)
            self.visit(node.left, scope)
            self.visit(node.right, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(UnaryExpressionNode)
    def visit(self, node: UnaryExpressionNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_unary_expression(node, local_scope)
            self.visit(node.value, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(LiteralExpressionNode)
    def visit(self, node: LiteralExpressionNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_literal_expression(node, local_scope)

            self.visit(node.value, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_expression_block(node, local_scope)
            for expression in node.expr_list:
                self.visit(expression, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(DynTestNode)
    def visit(self, node: DynTestNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_dyn_test(node, local_scope)

            self.visit(node.expr, scope)
            self.visit(node.type, scope)

        except SemanticError as ex:
            self.errors.append(ex.text)


    @visitor.when(LetNode)
    def visit(self, node: LetNode, local_scope: Collector_Info):
        try:
            scope = self.context.add_let(node, local_scope)
            #Visitar las asignaciones
            for assing in node.assign_list:
                self.visit(assing, scope)
            #visitar la expresion
            self.visit(node.expr, scope)
        except SemanticError as ex:
            self.errors.append(ex.text)





