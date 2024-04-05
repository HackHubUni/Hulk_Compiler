import cmp.visitor as visitor
from Hulk.tools.Ast import *
from cmp.ast import *
class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<stat>; ... <stat>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.decl_list)
        return f'{ans}\n{statements}'

    @visitor.when(TypeDeclarationNode)
    def visit(self, node, tabs=0):
       ans='\t' * tabs + f'\\TypeDeclaration con nombre {node.id} [def] de padre {node.parent}'
       features='Los features son:'
       features+= '\n'.join(self.visit(child, tabs + 1) for child in node.features)
       args='Los argumentos son'
       args+='\n'.join(self.visit(child, tabs + 1) for child in node.args)
       return f'{ans}\n{features}\n{args}'



    #@visitor.when(PrintNode)
    #def visit(self, node, tabs=0):
    #    ans = '\t' * tabs + f'\\__PrintNode <expr>'
    #    expr = self.visit(node.expr, tabs + 1)
    #    return f'{ans}\n{expr}'

    @visitor.when(VarDefNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    @visitor.when(ExpressionNode)
    def visit(self, node, tabs=0):
        return f'En el Expression Node'
    @visitor.when(MethodNode)
    def visit(self, node, tabs=0):
        params = ', '.join( str(element ) for element in node.args)
        ans = '\t' * tabs + f'\\__MethodNode Def: def {node.id}({params}) ->{node.return_type}'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'
    @visitor.when(FunctionDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({params}) -> <expr>'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(BinaryExpressionNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    @visitor.when(FunctionCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FunctionCallNode: {node.lex}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'
