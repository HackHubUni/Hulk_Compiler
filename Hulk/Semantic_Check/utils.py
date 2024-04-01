from cmp.semantic import  Context, SemanticError
from Hulk.Semantic_Check.type_node import *
class HulkContext(Context):
    def __init__(self):
        Context.__init__(self)
        self.function = {}

    def create_function(self, name, params, return_type):
        if name in self.function:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        for _param in params:
            if _param.type is None:
                _param.type = NoneType()
        typex = self.function[name] = Function(name, params, return_type)
        return typex

    def get_func(self, name: str):
        try:
            return self.func[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def create_protocol(self, name, parents):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Protocol(name, parents)
        return typex

    def __str__(self):
        types_str = 'Types: {\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'
        func_str = 'Functions: {\n\t' + '\n\t'.join(y for x in self.function.values() for y in str(x).split('\n')) + '\n}'
        return types_str + '\n' + func_str
