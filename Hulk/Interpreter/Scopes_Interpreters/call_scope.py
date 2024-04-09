from Hulk.Semantic_Check.basic_types.scopes import HulkScope
from Hulk.Semantic_Check.basic_types.semantic_types import *
from typing import Self
import copy
from enum import Enum
from Hulk.tools.Ast import VarNode


class Type_Scope(Enum):
    Program=-1
    Null = 0
    Func_Call = 1
    Type_Instantiate = 2
    Method_Instantiate = 3


class InterpreterScope:
    def __init__(self, scope: HulkScope, parent: Self = None, iter_count=0,it_from_program_node:bool=False):
        self.name: str = ""
        self.tag: Type_Scope = Type_Scope.Program if it_from_program_node else Type_Scope.Null
        self.scope = scope.clone()
        self.parent = parent
        self.childs = []
        self.args: dict[str:TypeContainer] = {}
        self.attrs:dict[str:TypeContainer]={}
        self.iteration_num = iter_count
        self.vector: dict[str:list] = {}
        #self.attrs:
        if self.iteration_num > 500:
            raise SemanticError(f"La StackOverFlow {500} llamados")

    def get_scope_child(self):
        new = CallScope(self.scope, self, self.iteration_num + 1)
        self.childs.append(new)
        return new

    def get_func_info_(self, name: str) -> FunctionInfo:
        try:
            return self.scope.functions[name]
        except KeyError:
            raise SemanticError(f'La función {name} no existe')

    def get_type_info_(self, name: str) -> TypeContainer:
        try:
            return self.scope.types[name]
        except KeyError:
            raise SemanticError(f'El type {name} no existe')

    def set_arg(self, name: str, typeContainer: TypeContainer):
        """
        Setea el argumento de la funcion o metodo o Type
        """
        if name in self.args:
            raise SemanticError(f'El argumento {name} ya existe')

        self.args[name] = typeContainer

    def set_attr(self,name: str, typeContainer: TypeContainer):
        if name in self.attrs:
            raise SemanticError(f'El atributo ya ha sido declarado: {name} no se puede mediante una asignación redefinir su valor')

        self.attrs[name] = typeContainer


    def set_func_call(self, name: str) -> FunctionInfo:
        self.tag = Type_Scope.Func_Call
        self.name = name
        return self.get_func_info_(name)

    def set_type_call(self, name: str) -> TypeContainer:
        """Le da nombre al nuevo al scope como el nombre de la instancia del type y devuelve su TypeInfo"""
        self.tag = Type_Scope.Type_Instantiate
        self.name = name
        return self.get_type_info_(name)

    def get_father_type_name_by_method(self,method_name:str)->str:
        if self.parent is None:
            raise SemanticError(f'El método {method_name} no existe en ningún type')
        if self.tag == Type_Scope.Method_Instantiate:
            return self.name
        return self.parent.get_father_type_name_by_method(method_name)
    def set_method_call(self,type_name:str,method_name:str)->TypeMethodInfo:
        self.tag = Type_Scope.Method_Instantiate
        self.name = method_name
        if type_name=="self":
            type_name=self.get_father_type_name_by_method(method_name)
        return self.get_method_info_(type_name,method_name)

    def get_method_info_(self,type_name:str,method_name:str)->TypeMethodInfo:
        try:
            type_i:TypeInfo=self.get_type_info_(type_name)
            return type_i.get_method(method_name)
        except KeyError:
            raise SemanticError(f'El método {method_name} no existe en el type {type_name}')



    def get_var_value(self, var_node_name: str)->TypeContainer:
        try:
            #Como el unico con parent=None es el Program node que no tiene variables
            if self.parent is None:
                raise SemanticError(f'La variable {var_node_name} no existe')

            if var_node_name in self.args:
                return self.args[var_node_name]

            return self.parent.get_var_value(var_node_name)

        except:
            raise SemanticError(f'La variable {var_node_name} no existe')

    def get_attr_value(self,attr_name:str)->TypeContainer:
        try:
            # Como el unico con parent=None es el Program node que no tiene ese atributo
            if self.parent is None:
                raise SemanticError(f'El atributo {attr_name} no existe')

            if attr_name in self.args:
                return self.attrs[attr_name]

            return self.parent.get_attr_value(attr_name)

        except:
            raise SemanticError(f'El atributo {attr_name} no existe')

class TypeInstantiateScope(InterpreterScope):
    def __init__(self, scope: HulkScope, parent: Self = None, iter_count=0):
        super().__init__(scope, parent, iter_count)()
        self.types_instantiates: dict[str, Self] = {}


class CallScope(InterpreterScope):

    def __init__(self, scope: HulkScope, parent: Self = None, iter_count=0,it_from_program_node:bool=False):
        super().__init__(scope, parent, iter_count,it_from_program_node)

        self.types_instantiates: dict[str, TypeInstantiateScope] = {}
