from Hulk.Semantic_Check.Scopes.Collector_Scope import Collector_Info
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


class Collector(object):
    """
    Recolecta toda la información relevante de los scopes del hulk
    """

    def __init__(self, errors=[]):
        self.context:Collector_Info = None
        self.errors = errors


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):

        self.context:Collector_Info = Collector_Info()
        # LLamar a cada declariacion del metodo
        for class_declaration in node.decl_list:
            self.visit(class_declaration)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node:ProtocolDeclarationNode):

        try:
            self.context.add_protocol(node)
        except SemanticError as ex:
            self.errors.append(ex.text)


    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode):
        try:
            context = self.context.add_type(node)


            for features in node.features:
                    self.visit(features, context)
            # Controlar la herencia cíclica


        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode:
        try:
            # Revisar que coincidan las variables
            name = node.id
            if not local_scope.contains_method(name):
                raise SemanticError(f'El metodo {name} en el type {local_scope.id} no está definido')
            vars = node.args
            # Redefinir el nuevo scope
            local_scope = MethodScope(local_scope, name, vars)

            body = node.body
            self.set_current_node(node)
            self.visit(body, local_scope)




        except SemanticError as ex:
            self.errors.append(ex.text)


