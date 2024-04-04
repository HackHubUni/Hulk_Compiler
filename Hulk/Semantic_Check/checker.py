from cmp import visitor
from cmp.semantic import Scope
from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_node import *
from Hulk.Semantic_Check.check_type_semantic import *
from Hulk.Semantic_Check.type_inferator import *



WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'


class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode, scope=None):
        scope = Scope()
        for declaration in node.decl_list:
            self.visit(declaration, scope.create_child())
        self.visit(node.expr, scope.create_child())
        return scope
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)            
        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AssignNode)
    def visit(self, node:AssignNode,scope):
        if not node.var.type is None:
            try:
                var_type=self.context.get_type(node.var.type)
            except SemanticError as ex:
                self.errors.append(ex.text)
                var_type = ErrorType()
        else:
            self.visit(node.expr, scope)
            var_type=node.expr.inferred_type
        if scope.is_defined(node.var.id):
            self.errors.append(LOCAL_ALREADY_DEFINED %(node.var.id, self.current_method.name) if self.current_method != None else LOCAL_ALREADY_DEFINED %(node.var.id, self.current_type.name))
        else:
            scope.define_variable(node.var.id, var_type)
        if not node.expr.inferred_type.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_TYPES %(node.expr.inferred_type.name, var_type.name))
        node.inferred_type = var_type

    @visitor.when(DestrAssign)
    def visit(self, node:DestrAssign,scope):

        if scope.is_defined(node.id):
            type=scope.find_variable(node.id)
            node.inferred_type=type.type
        self.visit(node.expr,scope)


    #============================= CallNodes ================================

    @visitor.when(AttrrCallNode)
    def visit(self, node,scope):
        node.inferred_type=StringType()    

    @visitor.when(MethodCallNode)
    def visit(self, node,scope):
        if scope.is_defined(node.obj):
            type=scope.find_variable(node.obj)
            obj_type=type.type
        else:
            self.errors.append(VARIABLE_NOT_DEFINED %(node.obj,'here'))

        
        try:
            method = obj_type.get_method(node.id)
            if not len(node.args) == len(method.param_types):
                self.errors.append(INVALID_OPERATION %(method.name, obj_type.name))
                node.inferred_type = ErrorType()
                return
            for i, arg in enumerate(node.args):
                self.visit(arg, scope)
                if not arg.inferred_type.conforms_to(method.param_types[i]):
                    self.errors.append(INCOMPATIBLE_TYPES %(arg.inferred_type, method.param_types[i]))
            node.inferred_type = method.return_type
        except SemanticError as ex:
            self.errors.append(ex.text)
            node.inferred_type = ErrorType()

    @visitor.when(FuncCallNode)
    def visit(self, node : FuncCallNode,scope):
        if node.id =='base':
            node.inferred_type=StringType()
        else:
            func = self.context.get_func(node.id)
            try:
                if not len(node.args) == len(func.param_names):
                    self.errors.append(INVALID_OPERATION %(func.name, node.id))
                    node.inferred_type = ErrorType()
                    return
                for i, arg in enumerate(node.args):

                    if isinstance(arg, VarNode):
                        if scope.is_defined(arg.lex):
                            type=scope.find_variable(arg.lex)
                            arg.inferred_type=type.type
                        else:
                            self.errors.append(VARIABLE_NOT_DEFINED %(node.obj,'here'))
                    else:
                        self.visit(arg, scope)    
                    if not arg.inferred_type.conforms_to(func.param_names[i].type):
                        self.errors.append(INCOMPATIBLE_TYPES %(arg.inferred_type, func.param_names[i].type))

                node.inferred_type=func.return_type
            except SemanticError as ex:
                self.errors.append(ex.text)
                node.inferred_type = ErrorType()

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        try:
            node.inferred_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            node.inferred_type = ErrorType()

    @visitor.when(MethodNode)
    def visit(self, node,scope):
        scope_child=scope.create_child()
        self.visit(node.body, scope_child)
        node.return_type=node.body.inferred_type
     
    @visitor.when(FunctionDeclarationNode)
    def visit(self, node : FunctionDeclarationNode,scope):
        for arg in node.args:
            if scope.is_defined(arg.id):
                self.errors.append(LOCAL_ALREADY_DEFINED %(node.var.id, self.current_method.name) if self.current_method != None else LOCAL_ALREADY_DEFINED %(node.var.id, self.current_type.name))
            else:
                scope.define_variable(arg.id, arg.type)
        self.visit(node.body, scope)
        node.return_type=node.body.inferred_type
        self.context.func[node.id].return_type=node.body.inferred_type



    #================================    MOVES   ====================================================

    @visitor.when(LetNode)
    def visit(self, node,scope):
        for declaration in node.assign_list:
            self.visit(declaration, scope)
        self.visit(node.expr, scope)

    @visitor.when(ExpressionBlockNode)
    def visit(self, node:ExpressionBlockNode,scope):
        for exrp in node.expr_list:
            self.visit(exrp, scope)
            node.inferred_type=exrp.inferred_type

    @visitor.when(IfNode)
    def visit(self, node,scope):
        self.visit(node.cond, scope)
        self.visit(node.if_expr, scope)
        for arg in node.elif_branches:
            self.visit(arg[0],scope)
            self.visit(arg[1],scope)
        self.visit(node.else_expr, scope)
        node.inferred_type=ObjectType()

    @visitor.when(WhileNode)
    def visit(self, node : WhileNode,scope):
        self.visit(node.cond, scope)
        self.visit(node.body, scope)
        node.inferred_type=node.body.inferred_type

    @visitor.when(ForNode)
    def visit(self, node : WhileNode,scope):
        self.visit(node.cond, scope)
        self.visit(node.body, scope)
        node.inferred_type=node.body.inferred_type


    @visitor.when(DynTestNode)
    def visit(self, node,scope):
        pass
        #self.visit(node.expr, scope.create_child())
        #if scope.is_defined(node.expr.lex):
            #var=scope.find_variable(node.expr.lex)
        #type=self.context.get_type(node.type)

        #if not type.conforms_to(var.type):
            #self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            #node.inferred_type = ErrorType()


    #================================ OPERATIONS ====================================================
    @visitor.when(PlusNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(NumType()) or not node.right.inferred_type.conforms_to(NumType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=NumType()

    @visitor.when(MinusNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(NumType()) or not node.right.inferred_type.conforms_to(NumType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=NumType()
        

    @visitor.when(DivNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(NumType()) or not node.right.inferred_type.conforms_to(NumType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=NumType()
        

    @visitor.when(StarNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(NumType()) or not node.right.inferred_type.conforms_to(NumType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=NumType()
        

    @visitor.when(ModNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(NumType()) or not node.right.inferred_type.conforms_to(NumType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=NumType()
        

    @visitor.when(PowNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(NumType()) or not node.right.inferred_type.conforms_to(NumType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=NumType()


    @visitor.when(NegativeNode)
    def visit(self, node,scope):
        if isinstance(node.node, VarNode):
            if scope.is_defined(node.node.lex):
                type=scope.find_variable(node.node.lex)
                node.node.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.node,'here'))
        self.visit(node.node, scope)

        
        if not node.node.inferred_type.conforms_to(NumType()):
            self.errors.append(INVALID_OPERATION %(node.node.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=NumType()

    @visitor.when(GeqNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
       
        if not node.left.inferred_type.conforms_to(node.right.inferred_type) or not node.right.inferred_type.conforms_to(node.left.inferred_type):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=BoolType()

    @visitor.when(LeqNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(node.right.inferred_type) or not node.right.inferred_type.conforms_to(node.left.inferred_type):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=BoolType()


    @visitor.when(GreaterNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(node.right.inferred_type) or not node.right.inferred_type.conforms_to(node.left.inferred_type):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=BoolType()

    @visitor.when(LessNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(node.right.inferred_type) or not node.right.inferred_type.conforms_to(node.left.inferred_type):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=BoolType()

    @visitor.when(EqualNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(node.right.inferred_type) or not node.right.inferred_type.conforms_to(node.left.inferred_type):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=BoolType()

    @visitor.when(NotEqualNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(node.right.inferred_type) or not node.right.inferred_type.conforms_to(node.left.inferred_type):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=BoolType()

    
    @visitor.when(NotNode)
    def visit(self, node,scope):

        if isinstance(node.node, VarNode):
            if scope.is_defined(node.node.lex):
                type=scope.find_variable(node.node.lex)
                node.node.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.node,'here'))
        self.visit(node.node, scope)

        
        if not node.node.inferred_type.conforms_to(BoolType()):
            self.errors.append(INVALID_OPERATION %(node.node.inferred_type.name))
            node.inferred_type = ErrorType()
        node.inferred_type=BoolType()

    @visitor.when(AndNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(BoolType()) or not node.right.inferred_type.conforms_to(BoolType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
        node.inferred_type=BoolType()
        

    @visitor.when(OrNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(BoolType()) or not node.right.inferred_type.conforms_to(BoolType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
        node.inferred_type=BoolType()
        

    @visitor.when(ConcatNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(StringType()) or not node.right.inferred_type.conforms_to(StringType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))
        node.inferred_type=StringType()

    @visitor.when(ConcatWithSpaceNode)
    def visit(self, node,scope):
        if isinstance(node.left, VarNode):
            if scope.is_defined(node.left.lex):
                type=scope.find_variable(node.left.lex)
                node.left.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.left.lex,'here'))
        else:
            self.visit(node.left, scope)

        if isinstance(node.right, VarNode):
            if scope.is_defined(node.right.lex):
                type=scope.find_variable(node.right.lex)
                node.right.inferred_type=type.type
            else:
                self.errors.append(VARIABLE_NOT_DEFINED %(node.right.lex,'here'))
        else:
            self.visit(node.right, scope)
        
        if not node.left.inferred_type.conforms_to(StringType()) or not node.right.inferred_type.conforms_to(StringType()):
            self.errors.append(INVALID_OPERATION %(node.left.inferred_type.name, node.right.inferred_type.name))

        node.inferred_type=StringType()





