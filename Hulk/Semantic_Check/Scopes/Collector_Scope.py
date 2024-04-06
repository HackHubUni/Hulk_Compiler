from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.Scopes.hulk_global_scope import HulkGlobalScope, TypeScope, MethodScope, FunctionScope
from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from typing import Self
from Hulk.Semantic_Check.Scopes.Base_Buildings import HulkBase

class HulkScope:
    def __init__(self,father:Self):
        self.father:HulkScope=father
        self.functions_decl:dict[str,FunctionDeclarationNode]
        self.functions_call:dict[str,FunctionCallNode]
        self.types_methods:dict[str,MethodNode]
        self.attr_:dict[str,AttrCallNode]

class Protocols_Info(HulkScope):
    def start(self):
        for method in self.prot_decl.methods:
            method_name = method.id
            if method_name in self.methods:
                raise SemanticError(
                    f'El protocolo {self.name} no puede tener dos definiciones del metodo {method_name}')
            self.methods[method_name] = method

    def __init__(self, prot_decl: ProtocolDeclarationNode):
        self.name: str = prot_decl.id
        self.parents: list[str] = prot_decl.parents
        self.childs: list[str] = []
        self.prot_decl: ProtocolDeclarationNode = prot_decl
        self.methods: dict[str, MethodNode] = {}
        self.start()


class Type_Info(HulkScope):

    def start_features_(self):
        for features in self.type_decl_.features:
            if isinstance(features, MethodNode):
                method: MethodNode = features
                method_name = method.id

                if method_name in self.methods_:
                    raise SemanticError(
                        f'El metodo {method_name} en el type: {self.name} no se puede declarar dos veces')

                self.methods_[method_name] = method
            elif isinstance(features, AssignNode):
                assing_attr: AssignNode = features
                assing_attr_name = assing_attr.var.id

                if assing_attr_name in self.assings_attr_:
                    raise SemanticError(f'El atributo {assing_attr_name} esta definido anteriormente en {self.name}')

    def start_args_(self):
        args: list[VarDefNode]=self.type_decl_.args
        for arg in args:
            arg_name=arg.id
            if arg_name in self.args_:
                raise SemanticError(f'No se puede tener dos argumentos {arg_name} iguales en el type: {self.name}')


    def start_(self):
        self.start_features_()
        self.start_args_()



    def __init__(self, type_decl: TypeDeclarationNode,father:HulkScope):
        super().__init__(father)
        super.self.attr_
        self.name = type_decl.id
        self.type_decl_: TypeDeclarationNode = type_decl
        self.assings_attr_:dict[str,AssignNode]={}
        self.methods_:dict[str,MethodNode]={}
        self.inherence_methods:dict[str,MethodNode]={}
        self.args_:dict[str,VarDefNode]={}





class Collector_Info(HulkScope):
    def __init__(self):
        self.protocols_: dict[str, ProtocolDeclarationNode] = {}
        self.prot_info_: dict[str, Protocols_Info] = {}
        self.types_: dict[str, TypeDeclarationNode] = {}
        self.types_info_:dict[str,Type_Info]={}

    def add_protocol(self, prot_decl: ProtocolDeclarationNode):
        name = prot_decl.id
        if name in self.protocols_:
            raise SemanticError(f'No pueden existir dos protocols con igual nombre {name}')
        self.protocols_[name] = prot_decl
        prot_info = Protocols_Info(prot_decl)
        self.protocols_[name] = prot_info

    def add_type(self, type_decl: TypeDeclarationNode):
        name = type_decl.id
        if name in self.types_:
            raise SemanticError(f'No pueden existir dos types con igual nombre {name}')

        self.types_info_[name]=Type_Info()
        return HulkScope()
