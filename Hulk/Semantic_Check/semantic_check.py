from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.Scopes.hulk_global_scope import HulkGlobalScope, TypeScope, MethodScope,FunctionScope


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
        self.context:HulkGlobalScope = None
        self.errors = errors

    def get_current_node(self):
        return self.context.get_current_node()
    def set_current_node(self,new_current):
        self.context.set_current_node(new_current)

    @visitor.on('node')
    def visit(self, node,local_scope=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node,local_scope=None):

        self.context = HulkGlobalScope(node)
        # LLamar a cada declariacion del metodo
        for class_declaration in node.decl_list:
            self.visit(class_declaration,self.context)



    @visitor.when(TypeDeclarationNode)

    def visit(self, node:TypeDeclarationNode,local_scope):
        try:
           context= self.context.create_type(node)
            #cambiar el current
           self.set_current_node(node)


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
           self.set_current_node(node)
           self.visit(body,local_scope)




       except SemanticError as ex:
           self.errors.append(ex.text)

    @visitor.when(DestructionAssignmentWithAttributeCallExpression)
    def visit(self, node: DestructionAssignmentWithAttributeCallExpression, local_scope: MethodScope):
        try:
            self.set_current_node(node)
            self.visit(node.attribute_call_expression,local_scope)
            self.set_current_node(node)
            self.visit(node.expression,local_scope)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(DestructionAssignmentBasicExpression)
    def visit(self, node: DestructionAssignmentBasicExpression, local_scope: MethodScope):
        try:
            self.set_current_node(node)
            self.visit(node, local_scope)
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
    def visit(self, node:VarNode, local_scope: MethodScope|HulkGlobalScope):
        try:
          name=str(node.value)
          if isinstance(local_scope,MethodScope):
              if not local_scope.is_var_define(name):
                  raise SemanticError(
                      f'La variable {name} no esta definida en este scope ni en ningun scope padre que redefina el método en caso de ser este heredado ')
          if isinstance(local_scope,FunctionScope):
              if not local_scope.is_var_arg(name):
                  raise (SemanticError
                         (f'La variable: {name} no esta definida en los argumentos de la función'))


        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(BinaryExpressionNode)
    def visit(self, node:BinaryExpressionNode, local_scope: MethodScope|HulkGlobalScope):
        try:
            self.set_current_node(node)
            self.visit(node.left,local_scope)
            self.set_current_node(node)
            self.visit(node.right,local_scope)

        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when( FunctionDeclarationNode)
    def visit(self, node:FunctionDeclarationNode,global_scope:HulkGlobalScope):
        try:



            self.set_current_node(node)
            self.visit(node.body,global_scope)

        except SemanticError as ex:
            self.errors.append(ex.text)


    @visitor.when(FunctionCallNode)
    def visit(self, node:FunctionCallNode, global_scope: HulkGlobalScope):
        try:
            name=node.id
            args=node.args
            func_scope:FunctionScope=global_scope.get_FunctionScope(name)
            if len(args)!=len(func_scope):
                raise SemanticError(f'La el llamado a la función {name } con {len(args)} es distinto a la cantidad requerida {len(func_scope)}')

        except SemanticError as ex:
            self.errors.append(ex.text)








