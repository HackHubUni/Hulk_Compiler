from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *


def parents_check(initial_type, parent):
    this_type = parent.name
    if initial_type == this_type:
        return True
    if parent.parent:
        return parents_check(initial_type, parent.parent)
    else:
        return False


class CheckTypes(object):
    """
    Recolecta toda la información relevante de los scopes del hulk
    """

    def __init__(self, errors=[]):
        self.global_scope: HulkScope = HulkScope(parent=None)
        self.errors = errors

    @visitor.on("node")
    def visit(self, node, scope: HulkScope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope: HulkScope):

        # Añadir al contexto los elementos primarios del hulk
        # TODO: Hay que cambiar la forma en que se ccede al contexto por las funciones que se agregaron al Hulk Cont
        self.global_scope.create_type("Num")
        self.global_scope.create_type("String")
        self.global_scope.create_type("Bool")
        self.global_scope.create_type("None")
        self.global_scope.create_type("Error")
        sin = FunctionDeclarationNode(
            "sin",
            [VarDefNode("angle", NumType())],
        )
        self.context.function["sin"] = self.context.create_function(
            "sin", [VarDefNode("angle", NumType())], NumType()
        )
        self.context.function["cos"] = self.context.create_function(
            "cos", [VarDefNode("angle", NumType())], NumType()
        )
        self.context.function["print"] = self.context.create_function(
            "print", [VarDefNode("value", ObjectType())], NoneType()
        )
        self.context.function["log"] = self.context.create_function(
            "log",
            [VarDefNode("base", NumType()), VarDefNode("value", NumType())],
            NumType(),
        )
        self.context.function["sqrt"] = self.context.create_function(
            "sqrt", [VarDefNode("value", NumType())], NumType()
        )
        self.context.function["exp"] = self.context.create_function(
            "exp", [VarDefNode("value", NumType())], NumType()
        )
        self.context.function["rand"] = self.context.create_function(
            "rand", [], NumType()
        )
        # LLamar a cada declariacion del metodo
        for declaration in node.decl_list:
            # Type Declaration
            # Protocol Declaration
            # Function Declaration
            self.visit(declaration)
        for exp in node.exp:
            # Let
            self.visit(exp)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node, scope: HulkScope):
        try:
            self.context.create_type(node.id)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(ProtDeclarationNode)
    def visit(self, node, scope: HulkScope):
        try:
            self.context.create_protocol(node.id, node.parents)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode, scope: HulkScope):
        try:
            if node.return_type == None:
                type = self.context.get_type("None")
                self.context.create_function(node.id, node.args, type)
            else:
                type = self.context.get_type(node.return_type)
                self.context.create_function(node.id, node.args, type)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(VarDefNode)
    def visit(self, node: Node, scope: HulkScope):
        try:
            self.context.create_variable(node.id, node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
