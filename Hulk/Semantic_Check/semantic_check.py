from Hulk.tools.Ast import *
from Hulk.Semantic_Check.to_replace.type_node import *
from Hulk.Semantic_Check.hulk_semantic_checker import *


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
        self.context:HulkChecker = None
        self.errors = errors



    @visitor.on('node')
    def visit(self, node,local_scope=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, local_scope=None):
        try:
            self.context = HulkChecker()
            self.visit(node.decl_list, self.context)
            self.visit(node.expr, self.context)
        except SemanticError as ex:
            self.errors.append(ex.text)
    #@visitor.when(TypeDeclarationNode)
    #def visit(self, node: TypeDeclarationNode, local_scope: HulkChecker):
    #    try:
    #        self.context = local_scope
    #        self.visit(node.type, self.context)
    #        self.visit(node.body, self.context)