from cmp.semantic import *
from Hulk.tools.Ast import *
from abc import ABC



class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, 'Object')


class NoneType(Type):
    def __init__(self):
        Type.__init__(self, 'None')


class NumType(ObjectType):
    def __init__(self):
        Type.__init__(self, 'Number')

    def __eq__(self, other:Type):
        return other.name == self.name or isinstance(other, NumType)


class StringType(ObjectType):
    def __init__(self):
        Type.__init__(self, 'String')

    def __eq__(self, other:Type):
        return other.name == self.name or isinstance(other, StringType)


class BoolType(ObjectType):
    def __init__(self):
        Type.__init__(self, 'Bool')

    def __eq__(self, other:Type):
        return other.name == self.name or isinstance(other, BoolType)


class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other:Type):
        return True

    def bypass(self):
        return True

    def __eq__(self, other:Type):
        return isinstance(other, Type)



   
        
class Function:
    def __init__(self, name, args, return_type):
        self.name = name
        self.param_names = args
        self.return_type = return_type

    def __str__(self):
        output = f'func {self.name}'
        output += ' ('
        params = ', '.join(f'{n.id}:{n.type.name}' for n in self.param_names)
        output += params
        output += ') :'
        output += self.return_type.name
        return output

    def __eq__(self, other:Type):
        return other.name == self.name and \
            other.return_type == self.return_type  # and \
        # other.param_types == self.param_types


class Protocol:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent:HulkScope = parent
        self.methods = []

    def define_method(self, name: str, param_names: list, param_types: list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def get_method(self, name: str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def __str__(self):
        output = f'protocol {self.name}'
        parent = '' if self.parent is None else ' : '.join(parent for parent in self.parent)
        output += ': ' + parent
        output += ' {'
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

class HulkScopeBase(ABC):
    pass
class HulkScope(HulkScopeBase):
    def __init__(self, parent:HulkScopeBase):
        self.parent: HulkScope = parent
        self.locals:dict[str:VariableInfo] = {}
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.types:dict[str,Type] = {}
        self.function:dict[str,Function]={}
        self.current:int=0
        self.ord:dict[Function|VariableInfo:int]={}
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
        var_str = 'Variables: {\n\t' + '\n\t'.join(y  for x in self.locals.keys() for y in str(x).split('\n')) + '\n}'
        return f'{types_str} \n  {func_str} \n {var_str}'

