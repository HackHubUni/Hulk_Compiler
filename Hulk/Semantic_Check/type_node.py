from cmp.semantic import Type, Context, SemanticError, Method


class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, 'Object')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, NumType) or isinstance(other, StringType) or isinstance(other, BoolType) or isinstance(other, ObjectType)

class NoneType(Type):
    def __init__(self):
        Type.__init__(self, 'None')


class NumType(ObjectType):
    def __init__(self):
        Type.__init__(self, 'Number')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, NumType) or isinstance(other, ObjectType)

class StringType(ObjectType):
    def __init__(self):
        Type.__init__(self,'String')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType) or isinstance(other, ObjectType)

class BoolType(ObjectType):
    def __init__(self):
        Type.__init__(self, 'Bool')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType) or isinstance(other, ObjectType)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class Function:
    def __init__(self,name,args,return_type):
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

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type #and \
            #other.param_types == self.param_types

class Protocol:
    def __init__(self,name:str,parent=None):
        """
         guarda el nombre del protocolo 
         padre del que hereda este
        """

        self.name=name
        self.parent = parent
        self.methods=[]

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def get_method(self, name:str):
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
        output +=': '+ parent
        output += ' {'
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output


