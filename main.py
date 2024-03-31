from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer
from Hulk.Parser.Hulk_Parser import get_hulk_parser
from Hulk.AST_Semantic.Ast import *

from cmp.evaluation import evaluate_reverse_parse

parser = get_hulk_parser()
print("Parser OKKK")
lexer = get_hulk_lexer()
print("Lexer and parser Ok")

text = ''' 

type Point {
    x = 0;
    y = 0;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
}
  print(4);

 '''

#text="function f(x,y) => (x+y);"

text = ''' type Point {
    x = 0;
    y = 0;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
}
type Bird inherits Superman {

}

type Plane inherits Bird{

}

type Superman inherits Plane {

}

function cot(x) => 1 / tan(x);
function tan(x) => sin(x) / cos(x);

let x = new Superman() in {
    print(
        if (x is Bird) "It's bird!"
        elif (x is Plane) "It's a plane!"
        else "No, it's Superman!"
    ); print(tan(PI) ** 2 + cot(PI) ** 2); }

 '''




tokens = lexer(text)



print(tokens)
parsedd, operationsdd = parser(tokens)
print(len(parsedd),"parser")
print(len(operationsdd),"operation")
print(len(tokens),"len tokens")


ast = evaluate_reverse_parse(parsedd, operationsdd, tokens)

