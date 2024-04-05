from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from typing import Self
from Hulk.Semantic_Check.Scopes.Base_Buildings import HulkBase

class Type_Scope:

    def control_protocol_methods(self, protocols_Methods: dict[str:ProtocolMethodNode], method: MethodNode):
        name = method.id
        if name in protocols_Methods:
            protocols_Methods.pop(name)
        return protocols_Methods
    def check_global_base_functions(self,method_name:str):
        if method_name in self.global_scope.base_function:
            raise SemanticError(f'El metodo {method_name} no puede ser definido es un valor base')
    def check_global_base_const(self,attr_name:str):
        if attr_name in self.global_scope.base_const:
            raise SemanticError(f' La constante {attr_name} no puede ser tomado como un atributo')

    def start(self, type_decl: TypeDeclarationNode, inherence_methods: dict[str:MethodNode],
              protocols_Methods: dict[str:ProtocolMethodNode]):

        for method in type_decl.features:
            if isinstance(method, MethodNode):

                name = method.id
                self.check_global_base_functions(name)
                # Controlar que se haya implementado lo de los protocolos
                protocols_Methods = self.control_protocol_methods(protocols_Methods, method)

                if name in self.methods:
                    if name in inherence_methods:
                        inherence_methods.pop(name)
                        self.methods[name] = method
                        continue
                    raise SemanticError(
                        f'Method with the same name ({name}) already in the context in type:{type_decl.id}.')
                else:
                    self.methods[name] = method

            elif isinstance(method, AssignNode):
                assing = method
                name = assing.var.id
                if name in self.assign:
                    raise SemanticError(
                        f'Assing con el mismo nombre {name} ya existe en el contexto del type:{type_decl.id}')
                else:
                    #Si no esta declarada se agrega al diccionario
                    self.assign[name]=assing
            else:
                raise SemanticError(f'El tipo {type(method)} no es de un metodo ni una asignacion')



         # implementar metodos de protocolos
        if len(protocols_Methods) > 0:
            raise SemanticError(f'Existen methods de protocolos sin implementar')



    def __init__(self, type_decl: TypeDeclarationNode, father: Self,global_scope:HulkBase, inherence_methods: dict[str:MethodNode] = {},
                 interface_methods: dict[str:ProtocolMethodNode] = {}):
        """
        Crea un nuevo scope para el nuevo type
        """
        self.global_scope=global_scope
        self.id = type_decl.id
        self.type_decl = type_decl
        self.father = father
        self.child: list[Type_Scope] = []
        self.inherence_methods: dict[str:MethodNode] = inherence_methods.copy()
        self.protocols_Methods: dict[str:ProtocolMethodNode] = interface_methods.copy()
        self.methods: dict[str:MethodNode] = {}
        self.assign: dict[str, AssignNode] = {}
        self.start(type_decl, inherence_methods.copy(), interface_methods.copy())
        print(0)

    def get_new_child_scope(self, type_decl: TypeDeclarationNode):
        child = Type_Scope(type_decl, self)
        self.child.append(child)
        return child


class HulkGlobalScope(HulkBase):
    function_decl: dict[str:FunctionDeclarationNode] = {}
    protocol_decl: dict[str:ProtocolDeclarationNode] = {}
    types_decl: dict[str:TypeDeclarationNode] = {}
    types_scope: dict[str:Type_Scope] = {}
    protocol_decl: dict[str:ProtocolDeclarationNode] = {}

    def create_function(self, func_node: FunctionDeclarationNode) -> bool:
        """
        Crear una función y guardarla en el scope global
        """
        name = func_node.id
        if name in self.function_decl:
            raise SemanticError(f'Function with the same name ({name}) already in the context.')
        self.function_decl[name] = func_node
        return True

    def create_protocol(self, protocol_node: ProtocolDeclarationNode):
        """
                Crear un protocolo  y guardarla en el scope global
                """
        name = protocol_node.id
        if name in self.function_decl:
            raise SemanticError(f'Protocol with the same name ({name}) already in the context.')
        self.function_decl[name] = protocol_node
        return True

    def create_type(self, type_node: TypeDeclarationNode) -> Type_Scope:
        """
        Crear un tipo y guardarlo en el scope global
        """

        name = type_node.id
        if name in self.types_decl:
            raise SemanticError(f'Type with the same name ({name}) already in the context.')
        self.types_decl[name] = type_node
        type_scope= Type_Scope(type_node, None, )
        self.types_scope[name]=type_scope
        return type_scope

    def __init__(self):
        super().__init__()
       # self.base_function:list[str]=["cos","sin","sqrt","exp","log","rand","print"]
       # self.base_const=["PI","E"]
        self.function_decl: dict[str:FunctionDeclarationNode] = {}
        self.protocol_decl: dict[str:ProtocolDeclarationNode] = {}
        self.types_decl: dict[str:TypeDeclarationNode] = {}
        self.types_scope: dict[str:Type_Scope] = {}
