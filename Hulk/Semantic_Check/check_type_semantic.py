from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.utils import HulkScope

def parents_check(initial_type, parent):
    this_type = parent.name
    if initial_type == this_type:
        return True
    if parent.parent:
        return parents_check(initial_type, parent.parent)
    else:
        return False


class InfoSaverTree(object):
    """
    Recolecta toda la información relevante de los scopes del hulk
    """
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):

        self.context = HulkScope() #Tomar el contexto del hulk
        # Añadir al contexto los elementos primarios del hulk
        self.context.types['Num'] = NumType()
        self.context.types['Str'] = StringType()
        self.context.types['Bool'] = BoolType()
        self.context.types['None'] = NoneType()
        self.context.types['<error>'] = ErrorType()
        self.context.function['sin'] = self.context.create_function('sin', [VarDefNode('angle', NumType())], NumType())
        self.context.function['cos'] = self.context.create_function('cos', [VarDefNode('angle', NumType())], NumType())
        self.context.function['print'] = self.context.create_function('print', [VarDefNode('value', ObjectType())], NoneType())
        self.context.function['log'] = self.context.create_function('log', [VarDefNode('base', NumType()),
                                                                            VarDefNode('value', NumType())], NumType())
        self.context.function['sqrt'] = self.context.create_function('sqrt', [VarDefNode('value', NumType())], NumType())
        self.context.function['exp'] = self.context.create_function('exp', [VarDefNode('value', NumType())], NumType())
        self.context.function['rand'] = self.context.create_function('rand', [], NumType())
        #LLamar a cada declariacion del metodo
        for declaration in node.decl_list:
            #Type Declaration
            #Protocol Declaration
            #Function Declaration
            self.visit(declaration)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(ProtDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_protocol(node.id, node.parents)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        try:
            if node.return_type == None:
                type = self.context.get_type('None')
                self.context.create_function(node.id, node.args, type)
            else:
                type = self.context.get_type(node.return_type)
                self.context.create_function(node.id, node.args, type)
        except SemanticError as ex:
            self.errors.append(ex.text)


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for class_declaration in node.decl_list:
            self.visit(class_declaration)
        

    @visitor.when(TypeDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        if node.parent:
            try:
                parent_type = self.context.get_type(node.parent)
                try:
                    self.current_type.set_parent(parent_type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
            except SemanticError as ex:
                self.errors.append(ex.text)
            if parents_check(self.current_type.name, self.current_type.parent):
                error = SemanticError("Herencia cíclica no admitida.")
                self.errors.append(error)
        for feature in node.features:
            self.visit(feature)

    @visitor.when(ProtDeclarationNode)
    def visit(self, node: ProtDeclarationNode):
        self.current_type = self.context.get_type(node.id)
        if node.parents:
            for parent in node.parents:
                try:
                    parent_type = self.context.get_type(parent)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                if parents_check(self.current_type.name, parent_type):
                    raise SemanticError("Herencia cíclica no admitida.")
        for feature in node.methods:
            self.visit(feature)

    @visitor.when(PrototypeMethodNode)
    def visit(self, node: PrototypeMethodNode):
        param_names = []
        param_types = []
        for args_name in node.args:
            param_names.append(args_name.id)
            if args_name.type == None:
                try:
                    param_type = self.context.get_type('None')
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            else:
                try:
                    param_type = self.context.get_type(args_name.type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            param_types.append(param_type)

        try:
            type = self.context.get_type(node.return_type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_method(node.id, param_names, param_types, type)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode):
        param_names = []
        param_types = []
        for args_name in node.args:
            param_names.append(args_name.id)
            if args_name.type == None:
                try:
                    param_type = self.context.get_type('None')
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            else:
                try:
                    param_type = self.context.get_type(args_name.type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
            param_types.append(param_type)

        try:
            type = self.context.get_type('None')
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_method(node.id, param_names, param_types, type)
        except SemanticError as ex:
            self.errors.append(ex.text)

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        try:
            type = self.context.get_type('None')
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_attribute(node.var.id, type)
        except SemanticError as ex:
            self.errors.append(ex.text)

