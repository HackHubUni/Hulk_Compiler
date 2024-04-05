from cmp.semantic import Context, SemanticError, Scope
from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *

class HulkGlobalScope(Context):
    function_decl: dict[str:FunctionDeclarationNode] = {}
    protocol_decl: dict[str:ProtocolDeclarationNode] = {}
    types_decl: dict[str:TypeDeclarationNode] = {}
    protocol_decl: dict[str:ProtocolDeclarationNode] = {}
    def create_function(self,func_node:FunctionDeclarationNode)->bool:
        """
        Crear una función y guardarla en el scope global
        """
        name=func_node.id
        if name in self.function_decl:
            raise SemanticError(f'Function with the same name ({name}) already in the context.')
        self.function_decl[name]=func_node
        return True
    def seed_func(self):
        self.context.function['sin'] = self.context.create_function('sin', [VarDefNode('angle', NumType())], NumType())
        plus=FunctionDeclarationNode("sin")



    def __init__(self):
        super().__init__()
        self.function_decl: dict[str:FunctionDeclarationNode] = {}
        self.protocol_decl: dict[str:ProtocolDeclarationNode] = {}
        self.types_decl: dict[str:TypeDeclarationNode] = {}
        self.protocol_decl:dict[str:ProtocolDeclarationNode]={}
