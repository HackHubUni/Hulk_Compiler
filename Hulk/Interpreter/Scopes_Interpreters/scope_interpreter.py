from Hulk.Interpreter.utils import *
from Hulk.Semantic_Check.basic_types.scopes import *
from Hulk.Semantic_Check.check_semantics import check_semantics
from Hulk.Semantic_Check.basic_types.scopes import *
import math
import random


class ScopeInterpreter:

    # scope.define_protocol('Iterable', self.context.get_protocol('Iterable'))
    def seed(self):
        self.define_function('print', print)
        self.define_function('sqrt', math.sqrt)
        self.define_function('sin', math.sin)
        self.define_function('cos', math.cos)
        self.define_function('exp', math.exp)
        self.define_function('log', math.log)
        self.define_function('rand', random.randint)
        self.define_function('range', range)



    def __init__(self, global_scope: HulkScopeLinkedNode, errors: list) -> None:
        self.global_scope = global_scope
        self.errors = errors
        self.call_functions_in_this_scope: dict[str, Callable] = {}
        self.dynamic_types: Dynamic_Types = Dynamic_Types(self.global_scope.get_all_types_names())
        self.seed()

    def define_function(self, name: str, function: Callable):
        """
        Define a function in the current scope
        """
        if name in self.call_functions_in_this_scope:
            self.errors.append(f"Function {name} already defined in this scope")

        self.call_functions_in_this_scope[name] = function

    def call_function(self, name: str, *args):
        """
        Call a function in the current scope
        """
        if name not in self.call_functions_in_this_scope:
            self.errors.append(f"Function {name} not defined in this scope")

        return self.call_functions_in_this_scope[name]


    def get_Type_Container(self,value,type_name:str|Dynamic_Types):
        """
        Devuelve el TypeContainer con el valor y el tag el tag puede ser un str o un Dynamic_Type
        """

        if isinstance(type_name,Dynamic_Types):
            return TypeContainer(value,type_name)
        elif isinstance(type_name,str):
            return TypeContainer(value,self.dynamic_types.get_tag(type_name))
        else:
            raise SemanticError("No Se entrego algo que no es un string o un Dynamic_Types")




    def is_this_Type(self,type_container:TypeContainer,type_name:str|Dynamic_Types)->bool:

        if isinstance(type_name,Dynamic_Types):
            return type_container.type == type_name
        elif isinstance(type_name,str):
            return type_container.type ==self.dynamic_types.get_tag(type_name)
        else:
            raise SemanticError("No Se entrego algo que no es un string o un Dynamic_Types")


    def get_variable(self, variable_name: str):
        return self.global_scope.get_variable(variable_name)



    def is_call_function_building_define(self,name:str)->bool:
        return name in self.call_functions_in_this_scope