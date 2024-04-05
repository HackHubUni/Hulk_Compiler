from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer
from Hulk.Parser.Hulk_Parser import get_hulk_parser
from Hulk.Draw_Ast.ast_visitor import *
from cmp.evaluation import evaluate_reverse_parse
#from Hulk.Semantic_Check.type_inferator import *
#from Hulk.Semantic_Check.type_node import *
#from Hulk.Semantic_Check.type_inferator import *
#from Hulk.Semantic_Check.checker import *
#from Hulk.Semantic_Check.type_node import *
#from Hulk.Semantic_Check.check_type_semantic import InfoSaverTree,TypeBuilder
from Hulk.Semantic_Check.semantic_check import SemanticChecker

# import lexer and parser
lexer = get_hulk_lexer()
parser = get_hulk_parser()

print("Lexer and parser Ok")


#text="function f(x,y) => (x+y);"


def evaluate(text:str):


        tokens = lexer(text)



        print(f"Los tokens son: \n {tokens}")
        #Parsear
        parse, operations = parser(tokens)

       # print(len(parse),"parser")
       # print(len(operations),"operation")
       # print(len(tokens),"len tokens")


        ast = evaluate_reverse_parse(parse, operations, tokens)

        #formatter = FormatVisitor()
        #print(formatter.visit(ast))



        errors = []

        collector = SemanticChecker(errors)
        collector.visit(ast)
        print(errors)
        #print(f"El ast es \n {ast}")
        #context = collector.context
#
        #builder = TypeBuilder(context, errors)
        #assert len(errors)==0, "No puede tener errores de semántica"
        #builder.visit(ast)
#
        #print('Errors:', errors)
        #print("contexto \n ", 'Context:')
        #print(context)
        #checker = TypeChecker(context, errors)
        #print(checker)
        #scope = checker.visit(ast)
        #print(scope)


text = ''' 


type Point {
    

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
    
    max() => self.getX();
    
    x = 0;
    y = 0;
}

type PolarPoint inherits Point {
    rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
    // ...
}

 '''

evaluate(text)






















