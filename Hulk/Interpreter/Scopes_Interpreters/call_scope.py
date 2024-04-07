from Hulk.Semantic_Check.basic_types.scopes import HulkScope
from Hulk.Semantic_Check.basic_types.semantic_types import *
from typing import Self
import copy
from enum import Enum
from Hulk.tools.Ast import VarNode




class Type_Scope(Enum):
    Null=0
    Func_Call=1



class CallScope:

    def __init__(self, scope: HulkScope, parent: Self = None):
        self.name:str=""
        self.tag:Type_Scope=Type_Scope.Null
        self.scope = scope.clone()
        self.parent = None
        self.childs = []
        self.args:dict[str:TypeContainer]={}





    def get_scope_child(self):
        new=CallScope(self.scope, self)
        self.childs.append(new)
        return new

    def get_func_info_(self,name:str)->FunctionInfo:
        try:
            return self.scope.functions[name]
        except KeyError:
            raise SemanticError(f'La función {name } no existe')

    def set_arg(self,name:str,typeContainer:TypeContainer):
        if name in self.args:
            raise SemanticError(f'El argumento {name} ya existe')

        self.args[name]=typeContainer

    def set_func_call(self,name:str)->FunctionInfo:
        self.tag=Type_Scope.Func_Call
        self.name=name
        return self.get_func_info_(name)

    def get_var_value(self,var_node_name:str):
        try:
            return self.args[var_node_name]
        except KeyError:
            raise SemanticError(f'La variable {var_node_name} no existe')









