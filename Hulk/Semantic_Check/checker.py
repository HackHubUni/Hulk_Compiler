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


class Checker(object):
    """
    Recolecta toda la información relevante de los scopes del hulk
    """

    def __init__(self, errors=[]):
        self.context: HulkGlobalScope = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, local_scope=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, local_scope=None):
        self.context = HulkGlobalScope(node)
        # LLamar a cada declariacion del metodo
        for class_declaration in node.decl_list:
            self.visit(class_declaration, self.context)
