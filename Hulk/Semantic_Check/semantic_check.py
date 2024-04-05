from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.Scopes.hulk_global_scope import HulkGlobalScope, TypeScope, MethodScope


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


class SemanticChecker(object):
    """
    Recolecta toda la información relevante de los scopes del hulk
    """

    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node,local_scope=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node,local_scope=None):
        self.context = HulkGlobalScope()
        # LLamar a cada declariacion del metodo
        for class_declaration in node.decl_list:
            self.visit(class_declaration,local_scope)

    @visitor.when(TypeDeclarationNode)

    def visit(self, node:TypeDeclarationNode,local_scope):
        try:
           context= self.context.create_type(node)

           for features in node.features:
               if isinstance(features,MethodNode):
                   pass
                   self.visit(features,context)
               else:
                   pass
                   self.visit(features, context)
           #Controlar la herencia cíclica

           if parents_check(context,context.father):
               error = SemanticError("Herencia cíclica no admitida.")
               self.errors.append(error)
               raise error

        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodNode)
    def visit(self, node:MethodNode, local_scope:TypeScope):
       try:
           # Revisar que coincidan las variables
           name=node.id
           if not  local_scope.contains_method(name):
               raise SemanticError(f'El metodo {name} en el type {local_scope.id} no está definido')
           vars = node.args
           #Redefinir el nuevo scope
           local_scope=MethodScope(local_scope,name,vars)


           body=node.body
           self.visit(body,local_scope)




       except SemanticError as ex:
           self.errors.append(ex.text)

    @visitor.when(DestructionAssignmentBasicExpression)
    def visit(self, node: DestructionAssignmentBasicExpression, local_scope: MethodScope):
        try:
            pass
        except SemanticError as ex:
        self.errors.append(ex.text)
    @visitor.when(AttrCallNode)
    def visit(self, node:AttrCallNode, local_scope:MethodScope):
        try:
           if not local_scope.is_attr_define(node.variable_id) :
               raise SemanticError(f'La variable {node.variable_id} no esta definida en este scope ni en ningun scope padre que redefina el método en caso de ser este heredado ')
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(VarNode)
    def visit(self, node: AttrCallNode, local_scope: MethodScope):
        print()







