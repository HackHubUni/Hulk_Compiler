from Hulk.Interpreter.scope_interpreter import ScopeInterpreter
from Hulk.Interpreter.utils import TypeContainer
from Hulk.Semantic_Check.basic_types.scopes import *
from Hulk.Semantic_Check.check_semantics import check_semantics
from Hulk.Semantic_Check.basic_types.scopes import *


class Interpreter(object):
    def __init__(self, context: HulkScopeLinkedNode, errors=[]):
        self.context = ScopeInterpreter(context, errors)
        self.errors: list[str] = errors
        self.is_this_type=self.context.is_this_Type

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):

        try:
            self.visit(node.expr)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode):
        for expr in node.expr_list:
            self.visit(expr)

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode):
        try:
            name = node.id
            temp: list[TypeContainer] = [self.visit(arg) for arg in node.args]
            args: list = []
            for i in temp:
                args.append(i.value)

            call = self.context.call_function(name)
            return call(args)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LiteralNumNode)
    def visit(self, node: LiteralNumNode):
        try:
            return self.context.get_Type_Container(float(node.value), "Number")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LiteralBoolNode)
    def visit(self, node: LiteralBoolNode):
        try:
            return self.context.get_Type_Container(bool(node.value), "Boolean")
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(LiteralStrNode)
    def visit(self, node: LiteralStrNode):
        try:
            return self.context.get_Type_Container(str(node.value), "String")
        except SemanticError as e:
            self.errors.append(e)

    #def get_binary_Num_expression(self, node:BinaryNumExpressionNode):
    #    left = self.visit(node.left)
    #    right = self.visit(node.right)
    #    #is_this_type = self.context.is_this_Type
    #    return left,right
    @visitor.when(BinaryNumExpressionNode)
    def visit(self, node: BinaryNumExpressionNode):
       try:
           op:str="sumar"
           value:float=0
           left = self.visit(node.left)
           right = self.visit(node.right)
           is_this_type = self.context.is_this_Type
           if not (self.is_this_type(left, "Number") and self.is_this_type(right, "Number")):
               raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")
           else:
               if isinstance(node,PlusNode):
                   value = left.value + right.value
                   op='+'
               elif isinstance(node,MinusNode):
                   value = left.value - right.value
                   op=''
               elif isinstance(node,DivNode):
                   value = left.value / right.value
                   op='/'
               elif isinstance(node,StarNode):
                   value = left.value * right.value
                   op='*'
               elif isinstance(node,ModNode):
                   value = left.value % right.value
                   op='%'
               elif isinstance(node,PowNode):
                   value = left.value ** right.value
                   op='**'
               else:
                   raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")

               return self.context.get_Type_Container(value, "Number")




       except SemanticError as e:
           self.errors.append(e)




    @visitor.when(BinaryBoolExpressionNode)
    def visit(self, node: BinaryBoolExpressionNode):
        try:
            #Por defecto es falso
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
                elif isinstance(node, NotNode):
                    value = not left.value
                elif isinstance(node, EqualNode):
                    value = left.value == right.value
                elif isinstance(node, NotEqualNode):
                    value = left.value != right.value
                elif isinstance(node,LessNode):
                    value = left.value < right.value
                elif isinstance(node,GreaterNode):
                    value = left.value > right.value
                elif isinstance(node,LeqNode):
                    value = left.value <= right.value
                elif isinstance(node,GeqNode):
                    value = left.value >= right.value
                else:
                    raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")

                return self.context.get_Type_Container(value, "Boolean")

        except SemanticError as e:
            self.errors.append(e)



    @visitor.when(BinaryStringExpressionNode)
    def visit(self, node:BinaryStringExpressionNode):
        try:
            value: str = ""

            left = self.visit(node.left)
            right = self.visit(node.right)
            #Si se puede concatenar con un numero
            #Si se puede concatenar con un string
            is_type_str:bool= (self.is_this_type(left, "String") and self.is_this_type(right, "String"))
            can_concat_with_number:bool=(self.is_this_type(left, "Number") and self.is_this_type(right, "String"))
            c=(self.is_this_type(left, "String") and self.is_this_type(right, "Number"))


            if not is_type_str or (can_concat_with_number or c):
                raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")
            else:
                l_val=str(left.value)
                r_val=str(right.value)
                if isinstance(node, ConcatNode):
                    value = l_val + r_val
                elif isinstance(ConcatWithSpaceNode):
                    return f'{l_val} {r_val}'
                else:
                    raise SemanticError(f"No se puede {type(node)} un {left.type} o un {right.type}")

                return self.context.get_Type_Container(value, "String")
        except SemanticError as e:
            self.errors.append(e)
