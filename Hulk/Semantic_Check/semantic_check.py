from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.Scopes.hulk_global_scope import HulkGlobalScope


def parents_check(initial_type, parent):
    this_type = parent.name
    if initial_type == this_type:
        return True
    if parent.parent:
        return parents_check(initial_type, parent.parent)
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

    def visit(self, node,local_scope):
        try:
           context= self.context.create_type(node)

           for features in node.features:
               if isinstance(features,MethodNode):
                   self.visit(features,context)
               else:
                   self.visit(features, context)

        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodNode)
    def visit(self, node, local_scope):
        try:
            context = self.context.create_type(node)

            for features in node.features:
                if isinstance(features, MethodNode):
                    self.visit(features, context)
                else:
                    self.visit(features, context)

        except SemanticError as ex:
            self.errors.append(ex.text)





