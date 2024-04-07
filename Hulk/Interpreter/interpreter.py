from Hulk.Interpreter.Scopes_Interpreters.call_scope import CallScope
from Hulk.Interpreter.Scopes_Interpreters.scope_interpreter import ScopeInterpreter
from Hulk.Interpreter.utils import TypeContainer
from Hulk.Semantic_Check.basic_types.scopes import *


class Interpreter(object):
    def __init__(self, context: HulkScopeLinkedNode, errors=[]):
        self.context = ScopeInterpreter(context, errors)
        self.errors: list[str] = errors
        self.is_this_type = self.context.is_this_Type

    def get_function(self, name: str) -> FunctionInfo:
        return self.context.global_scope.get_function(name)

    def get_new_Call_Scope(self, parent_scope: CallScope):
        return CallScope(self.context.global_scope.scope, parent_scope)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):

        try:
            parent_scope=self.get_new_Call_Scope(None)
            self.visit(node.expr, parent_scope)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode, parent_scope: CallScope):
        for expr in node.expr_list:
            self.visit(expr, parent_scope)

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode,parent_scope:CallScope):
       try:
           name = node.id
           new_scope = parent_scope.get_scope_child()
           args = []
           func_info = new_scope.set_func_call(name)
           arg_name=func_info.get_arguments_name()
           temp: list[TypeContainer] = [self.visit(arg, new_scope) for arg in node.args]

           for i,val in enumerate(temp,0):
               args.append(val.value)
               new_scope.set_arg(arg_name[i], val)
            # Si la funcion es building esta definida
           if self.context.is_call_function_building_define(name):
                call = self.context.call_function(name)
                return call(args)
           else:
                body=func_info.function_pointer.body
                return self.visit(body, new_scope)



       except SemanticError as e:
           self.errors.append(e)



    @visitor.when(VarNode)
    def visit(self, node: VarNode,parent_scope:CallScope)->TypeContainer:
        try:
                name=node.value
                return  parent_scope.get_var_value(name)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LiteralNumNode)
    def visit(self, node: LiteralNumNode,parent_scope:CallScope):
        try:
            return self.context.get_Type_Container(float(node.value), "Number")
        except SemanticError as e:
            self.errors.append(e)


    @visitor.when(LiteralBoolNode)
    def visit(self, node: LiteralBoolNode):
        try:
            if not isinstance(node.value, str):
                raise SemanticError(f"El {node.value} es de tipo {type(node.value)} no es str")
            val: str = node.value
            value = False if val.lower() == "false" else True
            return self.context.get_Type_Container(bool(value), "Boolean")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LiteralStrNode)
    def visit(self, node: LiteralStrNode):
        try:
            return self.context.get_Type_Container(str(node.value), "String")
        except SemanticError as e:
            self.errors.append(e)

    # def get_binary_Num_expression(self, node:BinaryNumExpressionNode):
    #    left = self.visit(node.left)
    #    right = self.visit(node.right)
    #    #is_this_type = self.context.is_this_Type
    #    return left,right
    @visitor.when(BinaryNumExpressionNode)
    def visit(self, node: BinaryNumExpressionNode,parent_scope:CallScope):
        try:
            op: str = "sumar"
            value: float = 0
            left = self.visit(node.left,parent_scope)
            right = self.visit(node.right,parent_scope)
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
    def visit(self, node: ConstantNode):
        try:
            var = self.context.get_variable(str(node.value))
            value = var.value
            return self.context.get_Type_Container(value, "Number")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(NegativeNode)
    def visit(self, node: NegativeNode):
        try:
            value = self.visit(node.value)
            return self.context.get_Type_Container(-value.value, "Number")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        try:
            value = self.visit(node.value)
            if not self.is_this_type(value, "Boolean"):
                raise SemanticError(f"{value.value} es de type {value.type} y no es de type Boolean")
            return self.context.get_Type_Container(not value.value, "Boolean")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(BinaryBoolExpressionNode)
    def visit(self, node: BinaryBoolExpressionNode):
        try:
            # Por defecto es falso
            value: bool = False

            left = self.visit(node.left)
            right = self.visit(node.right)
            if not (self.is_this_type(left, "Boolean") and self.is_this_type(right, "Boolean")):
                raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")
            else:
                if isinstance(node, AndNode):
                    value = left.value and right.value
                elif isinstance(node, OrNode):
                    value = left.value or right.value
                # elif isinstance(node, NotNode):
                #    value = not left.value
                elif isinstance(node, EqualNode):
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

                return self.context.get_Type_Container(value, "Boolean")

        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(BinaryStringExpressionNode)
    def visit(self, node: BinaryStringExpressionNode):
        try:
            value: str = ""

            left = self.visit(node.left)
            right = self.visit(node.right)
            # Si se puede concatenar con un numero
            # Si se puede concatenar con un string
            is_type_str: bool = (self.is_this_type(left, "String") and self.is_this_type(right, "String"))
            can_concat_with_number: bool = (self.is_this_type(left, "Number") and self.is_this_type(right, "String"))
            c = (self.is_this_type(left, "String") and self.is_this_type(right, "Number"))

            if not is_type_str or (can_concat_with_number or c):
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
    def visit(self, node: DynTestNode):
        try:

            visit = self.visit(node.expr)
            value: bool = self.is_this_type(visit, node.type)
            return self.context.get_Type_Container(value, "Boolean")
        except SemanticError as e:
            self.errors.append(e)

