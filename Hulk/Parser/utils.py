from Lexer_Parser.parser.shift_reduce import LR1Parser
from cmp.pycompiler import Token,Grammar
from Hulk.utils import contains_space

class Hulk_Parser_Container(LR1Parser):

    def __init__(self, G: Grammar, verbose=False):
        self.space=G.Get_Terminal("space") #Dado que cuando se haga call se tiene que quitar
        super().__init__(G,verbose)



    def __call__(self, w: list[Token]):

        lis=[]
        for token in w:
            if token.token_type.Name != self.space.Name:
                lis.append(token)

        assert not contains_space(lis), "La lista a pasar al parser tiene tokens space "

        return super().__call__(lis)
