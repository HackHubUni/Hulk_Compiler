from Lexer_Parser.Lexer.lexer import Lexer
from Hulk.tools.utils import contains_space
class HulkLexer(Lexer):

    def __call__(self, text):
        lis = []
        tokens = super().__call__(text)

        for token in tokens:
            if token.token_type.Name not in ["space","comments"] :
                lis.append(token)

        assert len(lis) > 0, "La lista no puede ser vacía"
        assert not contains_space(lis), "La lista que sale del Lexer tiene tokens space "

        return lis

