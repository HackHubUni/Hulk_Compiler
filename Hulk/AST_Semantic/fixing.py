from Hulk.Parser.Hulk_Parser import get_hulk_parser
from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer
from Lexer_Parser.shift_reduce import LR1Parser, evaluate_reverse_parse
from Hulk.AST_Semantic.Ast import *
import cmp.visitor as visitor

parser = get_hulk_parser()
print("Parser OKKK")
lexer = get_hulk_lexer()
print("Lexer and parser Ok")


def get_ast(code: str):
    return parser(lexer(code))







class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode {len(node.statements_list)}'

        statements = " "
        for statement in node.statements_list:
            asd = self.visit(statement, tabs + 1)
            print(asd)
            statements.join(asd)
        ans2 = f"COn {len(node.exp)}expresions"
        exps = " "
        for child in node.exp:
            print(type(child))
        exps = ''.join(self.visit(child, tabs + 1) for child in node.exp)

        return f"{ans} \n {statements}//{ans2}/{exps}"

    @visitor.when(NegNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: con lexema tipo{type(node.lex)} \n {self.visit(node.lex,tabs+1)}'

    @visitor.when(ConstantNumNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: con lexema {node.lex}'

    @visitor.when(StringExpression)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__StringExpression [<string-exp>;],<concatenable>'
        return ans

def parse(text: str):
    """
    Parsea la cadena, printea los token las producciones y las operaciones shift reduce adeams del ast
    :param text:
    :return:
    """
    all_tokens = lexer(text)
    tokens = list(filter(lambda token: token.token_type != 'space', all_tokens))
    print(f"Los tokens son {tokens}")
    right_parse, operations = parser(tokens)
    print(right_parse)
    print("-----------------------------")
    print(operations)
    print("###############################")
    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    # printer = get_printer(AtomicNode=ConstantNumberNode, BinaryNode=BinaryNode)
    # print(f" \n El ast es: \n {printer(ast)}")
    formatter = FormatVisitor()
    print(formatter.visit(ast))
def ff():
    print("Test 0")
    ast=get_ast('-5;')
    #parse('(let a = 4 in a) ')
    print("Finish test 0")

ff()