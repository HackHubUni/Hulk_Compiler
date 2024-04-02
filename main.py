from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer
from Hulk.Parser.Hulk_Parser import get_hulk_parser
# from Hulk.Semantic_Check.check_type_semantic import CheckTypes,TypeBuilder
from cmp.evaluation import evaluate_reverse_parse


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
        print(f"El ast es \n {str(ast)}")

        # errors = []
        # collector = CheckTypes(errors)
        # collector.visit(ast)
        # context = collector.context

        # builder = TypeBuilder(context, errors)
        # assert len(errors)==0, "No puede tener errores de semántica"
        # builder.visit(ast)
        
        # print('Errors:', errors)
        # print("contexto \n ", 'Context:')
        # print(context)




text = ''' 

  function hola (x){ x+a;}
  type Point {
     x = 0;
     y = 0;

     getX() => self.x;
     getY() => self.y;
  }

  type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
  }

  protocol Hashable {
     hash(): Number;
  }

  protocol Equatable extends Hashable {
     equals(other: Object): Boolean;
  }

  let a = 9 in print(a * 2);
  
 '''

evaluate(text)

