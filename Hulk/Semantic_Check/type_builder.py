from Hulk.tools.Ast import *
from basic_types.scopes import *
from basic_types.builtin_types import *
from basic_types.builtin_functions import *
from basic_types.builtin_protocols import *


class TypeBuilder:
    def __init__(self, scope: HulkScopeLinkedNode, errors: list) -> None:
        self.global_scope: HulkScopeLinkedNode = scope
        """This is the global scope of the program. Containing all the declarations"""
        self.errors = errors if len(errors) >= 0 else []
        """All the errors that the program contains"""
        self.current_type: TypeInfo = None
        """The current type that is been processed"""
        self.current_protocol: ProtocolInfo = None
        """The current protocol that is been processed"""

    @visitor.on("node")
    def visit(self, node: AstNode, scope: HulkScopeLinkedNode):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: HulkScopeLinkedNode):
        for declaration in node.declarations:
            self.visit(declaration, self.global_scope)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode, scope: HulkScopeLinkedNode):
        pass

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode, scope: HulkScopeLinkedNode):
        pass

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode, scope: HulkScopeLinkedNode):
        pass

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the declaration of a method
        inside a type. This type is stored in the variable self.current_type"""
        pass

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the assignment of a variable
        inside a type. This type is stored in the variable self.current_type"""
        pass

    @visitor.when(ProtocolMethodNode)
    def visit(self, node: ProtocolMethodNode, scope: HulkScopeLinkedNode):
        """This method is executed for processing the declaration of a method
        inside a protocol. This protocol type is stored in the variable self.current_protocol
        """
        pass
