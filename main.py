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

text="""


type Point {
    x = 0;
    y = 0;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
}
  print("hola");



"""
tokens = lexer(text)



print(tokens)
parsedd, operationsdd = parser(tokens)
print(len(parsedd),"parser")
print(len(operationsdd),"operation")
print(len(tokens),"len tokens")


ast = evaluate_reverse_parse(parsedd, operationsdd, tokens)
