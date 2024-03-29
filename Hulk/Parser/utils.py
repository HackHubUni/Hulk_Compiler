from Lexer_Parser.shift_reduce import LR1Parser
from cmp.pycompiler import Token,Grammar


def contains_space(lis: list[Token]):
    """
    True si la lista contien un token space
    """
    for token in lis:
        if token.is_space_token():
            return True
    return False
class Hulk_Parser_Container(LR1Parser):

    def __init__(self, G: Grammar, verbose=False):
        self.space=G.Get_Terminal("space")
        super().__init__(G,verbose)



    def __call__(self, w: list[Token]):

        lis=[]
        for token in w:
            if token.token_type.Name != self.space.Name:
                lis.append(token)
        assert not contains_space(lis), "La lista a pasar al parser tiene tokens space "
        super().__call__(lis)
