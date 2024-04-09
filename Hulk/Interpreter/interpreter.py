from Hulk.Interpreter.Scopes_Interpreters.call_scope import CallScope
from Hulk.Interpreter.Scopes_Interpreters.scope_interpreter import ScopeInterpreter
from Hulk.Interpreter.utils import TypeContainer
from Hulk.Semantic_Check.basic_types.scopes import *


class Interpreter(object):
    def __init__(self, context: HulkScopeLinkedNode, errors=[]):
        self.context = ScopeInterpreter(context, errors)
        self.errors: list[str] = errors
        self.is_this_type = self.context.is_this_Type
        self.max_iteration=5000

    def get_function(self, name: str) -> FunctionInfo:
        return self.context.global_scope.get_function(name)

    def get_new_Call_Scope(self, parent_scope: CallScope):
        return CallScope(self.context.global_scope.scope, parent_scope)

    def get_Type_Container(self, value, type_name: str | Dynamic_Types):
        return self.context.get_Type_Container(value, type_name)

    def get_NullTypeContainer(self, value=None):
        return self.context.get_NullTypeContainer(value)

    def get_UnknowTypeContainer(self, value):
        return self.context.get_UnknownTypeContainer(value)

    def is_NullTypeContainer(self,type_container:TypeContainer):
        return  isinstance(type_container,NullTypeContainer)

    def is_UnknowTypeContainer(self,type_container:TypeContainer):
        return  isinstance(type_container,UnknownTypeContainer)

    def is_true_expr(self,name:str):
        if isinstance(name,bool):
            return name
        return name in  ["TRUE,True,true"]

    def is_false_expr(self,name:str):
        if isinstance(name,bool):
            return not name
        return name in  ["FALSE,False,false"]

    def assing_var_exp(self,var_assig:TypeContainer,expr_to_assing:TypeContainer):
        """
        Chequea  si el var_assing tiene el mismo type de la expression asignada
        Si el tipo del var_assig es unknown devuelve le asigna a la variable el tipo de la expression
        """
        if self.is_UnknowTypeContainer(var_assig):
            var_assig.type=expr_to_assing.type
        elif var_assig.type!=expr_to_assing.type:
            raise SemanticError(f"La variable tiene el type:{var_assig.type} y la expresión tiene el type:{expr_to_assing.type}")

        return True
    @visitor.on('node')
    def visit(self, node):
        pass
  #Los scopes que se pasan siempre se forkea del padre
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):

        try:
            parent_scope = self.get_new_Call_Scope(None)
            self.visit(node.expr, parent_scope)

            #for decl in node.declarations:
            #    if isinstance(decl,TypeDeclarationNode):
            #        decl:TypeDeclarationNode=decl
            #        feat=decl.features
            #        for v in feat:
            #            if isinstance(v,AssignNode):
            #                v:AssignNode = v
            #                if isinstance(v.expression_to_evaluate,InstantiateNode):
            #                     self.visit(v.expression_to_evaluate, parent_scope)


        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode, parent_scope: CallScope):
        for expr in node.expr_list:
            self.visit(expr, parent_scope)

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, parent_scope: CallScope):
        try:
            name = node.id
            new_scope = parent_scope.get_scope_child()
            args = []
            func_info = new_scope.set_func_call(name)
            arg_name = func_info.get_arguments_name()
            temp: list[TypeContainer] = [self.visit(arg, new_scope) for arg in node.args]

            for i, val in enumerate(temp, 0):
                if val is None:
                    raise SemanticError(f"No pueden ver argumentos en la función {name} None")
                args.append(val.value)
                new_scope.set_arg(arg_name[i], val)
            # Si la funcion es building esta definida
            if self.context.is_call_function_building_define(name):
                call = self.context.call_function(name)
                type_name = "Unknown"
                if name in ["sin", 'cos', 'exp', 'log', 'sqrt', "rand"]:
                    args = args[0]
                    type_name = "Number"

                return self.context.get_Type_Container(call(args), type_name)

            else:
                body = func_info.function_pointer.body
                return self.visit(body, new_scope)



        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, parent_scope: CallScope):
        try:
            name =node.type_id
            new_scope=parent_scope.get_scope_child()
            type_info:TypeInfo=new_scope.get_type_info_(name)
            args_name:list[str]=type_info.get_args_name()
            args = []
            temp: list[TypeContainer] = [self.visit(arg, new_scope) for arg in node.initialization_expressions]
            for i, val in enumerate(temp, 0):
                if val is None:
                    raise SemanticError(f"No pueden ver argumentos en la función {name} None")
                args.append(val.value)
                new_scope.set_arg(args_name[i], val)



            #Instanciar los atributos
            attrs=type_info.attributes
            attrs_name:list[str]=[]
            varx=[]
            #Tomar los nombres de los atributos
            for attr in attrs.values():
                name=attr.name
                varx.append(var)
                attrs_name.append(name)
                var:TypeContainer=self.visit(attr.initialization_expression,parent_scope)
                new_scope.set_arg(name,var)


            #Ahora hay que instanciar los métodos
            methods_info=type_info.methods

            for method_name, method_info in methods_info.items():
                method = method_info.declaration_pointer
                self.visit(method, new_scope)


        except SemanticError as e:
            self.errors.append(e)




    @visitor.when(LetNode)
    def visit(self, node: LetNode, parent_scope: CallScope):
        try:

            new_scope=parent_scope.get_scope_child()
            #Por cada asignacion hace visit al varDefNode para agregarla al scope
            for arg in node.assign_list:
                self.visit(arg, new_scope)

            return self.visit(node.expr, new_scope)






        except SemanticError as e:
            self.errors.append(e)



    @visitor.when(AssignNode)
    def visit(self,node:AssignNode,parent_scope: CallScope):
        """
        Asigna en el scope padre el valor de la expresión de la variable
        """
        try:
             var_name=self.visit(node.var_definition, parent_scope)
             expr=self.visit(node.expression_to_evaluate, parent_scope)
             #Chequear que la expresión sea del mismo tipo que la variable
             self.assing_var_exp(var_name,expr)
             name_var:str=var_name.value
             parent_scope.set_arg(name_var,expr)
        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(VarDefNode)
    def visit(self, node: VarDefNode, parent_scope: CallScope):
        try:
            var_name=node.var_name
            type_name = node.var_type
            if type_name is None:
                return self.get_UnknowTypeContainer(var_name)

            return self.get_Type_Container(var_name,type_name)

        except SemanticError as e:
            self.errors.append(e)
    @visitor.when(VarNode)
    def visit(self, node: VarNode, parent_scope: CallScope) -> TypeContainer:
        try:
            name: str = node.value
            return parent_scope.get_var_value(name)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LiteralNumNode)
    def visit(self, node: LiteralNumNode, parent_scope: CallScope):
        try:
            return self.context.get_Type_Container(float(node.value), "Number")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LiteralBoolNode)
    def visit(self, node: LiteralBoolNode, parent_scope: CallScope):
        try:
            if not isinstance(node.value, str):
                raise SemanticError(f"El {node.value} es de tipo {type(node.value)} no es str")
            val: str = node.value
            value = False if val.lower() == "false" else True
            return self.context.get_Type_Container(bool(value), "Boolean")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LiteralStrNode)
    def visit(self, node: LiteralStrNode, parent_scope=CallScope):
        try:
            return self.context.get_Type_Container(str(node.value), "String")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(BinaryNumExpressionNode)
    def visit(self, node: BinaryNumExpressionNode, parent_scope: CallScope):
        try:
            op: str = "sumar"
            value: float = 0
            left = self.visit(node.left, parent_scope)
            right = self.visit(node.right, parent_scope)
            is_this_type = self.context.is_this_Type
            if not (self.is_this_type(left, "Number") and self.is_this_type(right, "Number")):
                raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")
            else:
                if isinstance(node, PlusNode):
                    value = left.value + right.value
                    op = '+'
                elif isinstance(node, MinusNode):
                    value = left.value - right.value
                    op = ''
                elif isinstance(node, DivNode):
                    value = left.value / right.value
                    op = '/'
                elif isinstance(node, StarNode):
                    value = left.value * right.value
                    op = '*'
                elif isinstance(node, ModNode):
                    value = left.value % right.value
                    op = '%'
                elif isinstance(node, PowNode):
                    value = left.value ** right.value
                    op = '**'
                else:
                    raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")

                return self.context.get_Type_Container(value, "Number")

        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(ConstantNode)
    def visit(self, node: ConstantNode, parent_scope: CallScope):
        try:
            var = self.context.get_variable(str(node.value))
            value = var.value
            return self.context.get_Type_Container(value, "Number")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(NegativeNode)
    def visit(self, node: NegativeNode, parent_scope: CallScope):
        try:
            value = self.visit(node.value, parent_scope)
            check: bool = self.is_this_type(value, "Number")
            if not check:
                raise SemanticError(f'{value.value}'' es de type {value.type} y no es de type Number')
            return self.context.get_Type_Container(-value.value, "Number")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(NotNode)
    def visit(self, node: NotNode, parent_scope: CallScope):
        try:
            value = self.visit(node.value, parent_scope)
            if not self.is_this_type(value, "Boolean"):
                raise SemanticError(f"{value.value} es de type {value.type} y no es de type Boolean")
            return self.context.get_Type_Container(not value.value, "Boolean")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(BinaryBoolExpressionNode)
    def visit(self, node: BinaryBoolExpressionNode, parent_scope: CallScope):
        try:
            # Por defecto es falso
            value: bool = False

            left = self.visit(node.left, parent_scope)
            right = self.visit(node.right, parent_scope)
            if  (self.is_this_type(left, "Boolean") and self.is_this_type(right, "Boolean")):
                if isinstance(node, AndNode):
                    value = left.value and right.value
                elif isinstance(node, OrNode):
                    value = left.value or right.value
             #   raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")
            else:

                # elif isinstance(node, NotNode):
                #    value = not left.value
                if isinstance(node, EqualNode):
                    value = left.value == right.value
                elif isinstance(node, NotEqualNode):
                    value = left.value != right.value
                elif isinstance(node, LessNode):
                    value = left.value < right.value
                elif isinstance(node, GreaterNode):
                    value = left.value > right.value
                elif isinstance(node, LeqNode):
                    value = left.value <= right.value
                elif isinstance(node, GeqNode):
                    value = left.value >= right.value
                else:
                    raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")

                if value is None :
                    raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")
                return self.context.get_Type_Container(value, "Boolean")

        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(BinaryStringExpressionNode)
    def visit(self, node: BinaryStringExpressionNode, parent_scope: CallScope):
        try:
            value: str = ""

            left = self.visit(node.left, parent_scope)
            right = self.visit(node.right, parent_scope)
            # Si se puede concatenar con un numero
            # Si se puede concatenar con un string
            is_type_str: bool = (self.is_this_type(left, "String") and self.is_this_type(right, "String"))
            can_concat_with_number: bool = (self.is_this_type(left, "Number") and self.is_this_type(right, "String"))
            c = (self.is_this_type(left, "String") and self.is_this_type(right, "Number"))

            if not is_type_str and not (can_concat_with_number or c):
                raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")
            else:
                l_val = str(left.value)
                r_val = str(right.value)
                if isinstance(node, ConcatNode):
                    value = l_val + r_val
                elif isinstance(ConcatWithSpaceNode):
                    return f'{l_val} {r_val}'
                else:
                    raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")

                return self.context.get_Type_Container(value, "String")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(DynTestNode)
    def visit(self, node: DynTestNode, parent_scope: CallScope):
        try:

            visit = self.visit(node.expr, parent_scope)
            value: bool = self.is_this_type(visit, node.type)
            return self.context.get_Type_Container(value, "Boolean")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(IfNodeExpression)
    def visit(self, node: IfNodeExpression, parent_scope: CallScope):
        try:
            if_exp: TypeContainer = self.visit(node.conditional_expression, parent_scope)
            bool_value = if_exp.value
            # Si la expresion del if_ condicional no es Boolean
            # dar error
            if not self.is_this_type(if_exp, "Boolean"):
                raise SemanticError(f'La expresión condicional {if_exp} no es Boolean es {if_exp.type}')
            # Comprobar si es True
            if  self.is_true_expr(bool_value):
                return self.visit(node.if_body_expression, parent_scope)
            # COmprobar que devolvio false
            elif self.is_false_expr(bool_value):
                # Ver por las ramas Elif
                elifb = self.visit(node.elif_branches, parent_scope)
                # Comprobar que las ramas elif no son NUll
                if not self.is_NullTypeContainer(elifb):
                    return elifb
                else:
                    return self.visit(node.else_expression, parent_scope)
            else:
                raise SemanticError(f'El tipo {bool_value} del value no es Boolean')

        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(ElifNodeExpressionList)
    def visit(self, node: ElifNodeExpressionList, parent_scope: CallScope):
        try:
            if node.elif_expressions is None or len(node.elif_expressions) == 0:
                return self.get_NullTypeContainer()
            for expr in node.elif_expressions:
                visit: TypeContainer = self.visit(expr, parent_scope)
                type = visit.type
                if self.is_true_expr(type):
                    return visit
                elif not self.is_false_expr(type):
                    raise SemanticError(f'El tipo {type} del value no es Boolean')

            # Si no hay ninguna rama que se cumpla
            return self.get_NullTypeContainer()

        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(ElifNodeAtomExpression)
    def visit(self, node: ElifNodeAtomExpression, parent_scope: CallScope):
        try:
            if_exp: TypeContainer = self.visit(node.conditional_expression, parent_scope)
            if not self.is_this_type(if_exp, "Boolean"):
                raise SemanticError(f'La expresión condicional {if_exp} no es Boolean es {if_exp.type}')
            type = if_exp.type
            if self.is_true_expr(type):
                return self.visit(node.body_expression, parent_scope)
            elif not self.is_false_expr(type):
                raise SemanticError(f'El tipo {type} del value no es Boolean')

        except SemanticError as e:
            self.errors.append(e)

    def while_condition(self,node:WhileExpressionNode,parent_scope:CallScope):
        if_exp: TypeContainer = self.visit(node.conditional_expression, parent_scope)
        bool_value:bool = if_exp.value
        if not isinstance(bool_value,bool):
            raise SemanticError(f'La expresión condicional {if_exp} no es Boolean es {if_exp.type}')
        # Si la expresion del if_ condicional no es Boolean
        # dar error
        if not self.is_this_type(if_exp, "Boolean"):
            raise SemanticError(f'La expresión condicional {if_exp} no es Boolean es {if_exp.type}')
        return bool_value
    @visitor.when(WhileExpressionNode)
    def visit(self,node:WhileExpressionNode,parent_scope:CallScope):
        try:
           i=0
           #Mientras se cumpla la condición visita la body expr
           while self.while_condition(node,parent_scope):
               if i>self.max_iteration:
                   raise SemanticError(f"StackOverFlow")
               i+=1
               self.visit(node.body_expression, parent_scope)


        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(VectorNode)
    def visit(self, node: VectorNode, parent_scope: CallScope):
        try:
            lis=[]
            for expr,i in enumerate(node.expression_list,0):
                temp=self.visit(expr,parent_scope)
                lis.append(temp)
                 #TODO:Falta chequear que sean del mismo tipo

            return self.context.get_Type_Container(lis, "Vector")
        except SemanticError as e:
            self.errors.append(e)



