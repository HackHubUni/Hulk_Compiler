from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer
from Hulk.Parser.Hulk_Parser import get_hulk_parser
from Hulk.AST_Semantic.check_type_semantic import InfoSaverTree,TypeBuilder


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





def evaluate(text:str):


        tokens = lexer(text)



        print(tokens)
        parsedd, operationsdd = parser(tokens)
        print(len(parsedd),"parser")
        print(len(operationsdd),"operation")
        print(len(tokens),"len tokens")


        ast = evaluate_reverse_parse(parsedd, operationsdd, tokens)

        errors = []
        collector = InfoSaverTree(errors)
        collector.visit(ast)
        print(f"El ast es \n {ast}")
        context = collector.context

        builder = TypeBuilder(context, errors)
        assert len(errors)==0, "No puede tener errores de semántica"
        builder.visit(ast)

        print('Errors:', errors)
        print("contexto \n ", 'Context:')
        print(context)


def test():
    test = ['let msg = "Hello" in print(msg);',
            ' let number = 42, test = "The meaning of life is" in print(test@@number);',
            'let number = 42 in (let text = "The meaning of life is" in ( print(test@number)));',
            'let a = 6, b = a*7 in print(b);',
            'let a=7, b=10,c=20 in {print(a);print(b);print(c);};',
            'let a = (let b =6 in b*7) in print(a);',
            'print(let b =6 in b*7);',
            'let a =20 in {let a =42 in print (a); print(a);};',
            'let a=0 in {print(a); a := 1; print(a);};',
            'let a =0 in let b = a := 1 in {print(a); print(b);};',
            'let a = 42 in if (a == 2) print(1) else print(2);',
            'let a = 2 in if (a ==2) {print(1);} else print(2);']

    for text in test:
        evaluate(text)