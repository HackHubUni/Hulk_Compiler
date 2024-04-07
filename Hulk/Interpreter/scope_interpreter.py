from Hulk.Semantic_Check.basic_types.scopes import *
from Hulk.Semantic_Check.check_semantics import check_semantics
from Hulk.Semantic_Check.basic_types.scopes import *
import math
import random
class ScopeInterpreter:


    #scope.define_protocol('Iterable', self.context.get_protocol('Iterable'))
    def seed(self):
        self.define_function('print', print)
        self.define_function('sqrt', math.sqrt)
        self.define_function('sin', math.sin)
        self.define_function('cos', math.cos)
        self.define_function('exp', math.exp)
        self.define_function('log', math.log)
        self.define_function('rand', random.randint)
        self.define_function('range', range)
        

    def __init__(self, ast: AstNode, global_scope: HulkScopeLinkedNode, errors: list) -> None:
        self.ast = ast
        self.global_scope = global_scope
        self.errors = errors
        self.call_functions_in_this_scope:dict[str,Callable]={}





    def define_function(self,name:str, function:Callable):
        """
        Define a function in the current scope
        """
        if name in self.call_functions_in_this_scope:
            self.errors.append(f"Function {name} already defined in this scope")

        self.call_functions_in_this_scope[name]=function





