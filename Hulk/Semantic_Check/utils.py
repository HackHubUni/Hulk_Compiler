from cmp.semantic import  SemanticError, VariableInfo,Type
from typing import Self
from Hulk.Semantic_Check.type_node import *
import itertools as itt

class HulkScope():
    def __init__(self, parent: Self):
        self.parent: Self = parent
        self.locals = {str:VariableInfo}
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.types:dict[str,Type] = {}

#let x=0 in (let y=0 in print(x+y))
    def create_child(self):
        child = HulkScope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname:str, vtype):
        """Create a new variable in the actual scope"""
        info = VariableInfo(vname, vtype)
        if vname in self.locals:
            raise SemanticError(f'The variable: {vname} is already defined')
        self.locals[vname] = info
        return info

    def find_variable(self, vname:str):
        """Try to find the variable in the local scope and if it is not in here
        it tries to find it in the parent scope.
        And if the variable is not in any of the parent scopes it raise a semantic error"""
        if vname in self.locals:
            return self.locals[vname]
        if not self.parent:
            raise SemanticError(f'The variable {vname} is not defined')
        return self.parent

    def is_var_defined(self, vname)->bool:
        try:
            self.find_variable(vname)
            return True
        except:
            return False

    def is_var_local(self, vname):
        return vname in self.locals

    def create_type(self, name:str):
        """
        Crea un Type dentro del Scope
        """
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')


    def create_function(self, name, params, return_type):
        if name in self.function:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        for _param in params:
            if _param.type is None:
                _param.type = NoneType()
        typex = self.function[name] = Function(name, params, return_type)
        return typex

    def create_protocol(self, name, parents):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Protocol(name, parents)
        return typex

    def __str__(self):
        types_str = 'Types: {\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'
        func_str = 'Functions: {\n\t' + '\n\t'.join(y for x in self.function.values() for y in str(x).split('\n')) + '\n}'
        var_str = 'Variables: {\n\t' + '\n\t'.join(y  for x in self.locals.values() for y in str(x).split('\n')) + '\n}'
        return f'{types_str} \n  {func_str} \n {var_str}'
