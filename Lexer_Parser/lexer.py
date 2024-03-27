try:
    from pycompiler import Token
    from automata import State
    from regx import RegexSimple
except:
    from cmp.pycompiler import Token
    from Lexer_Parser.automata import State
    from Lexer_Parser.regx import RegexSimple

class Lexer:
    def __init__(self, table, eof):
        """

        :param table: La tabla tiene que tener (valor, regex) osea es una lista de tuplas
        :param eof: G.EOF
        """
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):

            states = State.from_nfa(RegexSimple(regex).automaton())            
            for state in states:
                if state.final:
                    state.tag = (n, token_type)
            regexs.append(states)
        return regexs
    
    def _build_automaton(self):
        start = State('start')        
        for initial_state in self.regexs:
            start.add_epsilon_transition(initial_state)   
        return start.to_deterministic()
    
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''

        for symbol in string:            
            new_state = state[symbol]
            if new_state is not None:
                new_state = new_state[0]
                lex += symbol
                if new_state.final:
                    if new_state.tag is None:
                        fil = list(
                            map(lambda sub_state: sub_state.tag,
                                filter(lambda sub_state: sub_state.tag is not None,
                                    new_state.state))
                        )
                        assert len(fil) > 0, 'Mal Lexer'
                        new_state.tag = fil
                    final = new_state
                    final_lex = lex
                state = new_state
            else:
                break
            
        return final, final_lex
    
    def _tokenize(self, text):
        row = 0
        col = 0
        while len(text) > 0:
            final, final_lex = self._walk(text)
            tag, token_type = min(final.tag)
            yield final_lex, token_type, row, col

            splited = final_lex.split('\n')
            if len(splited) > 1:
                row += len(splited) - 1
                col = 0            
            col += len(splited[-1])

            text=text[len(final_lex):]
        
        yield '$', self.eof, row, col
    
    def __call__(self, text):
        return [ Token(lex, ttype, row, col) for lex, ttype, row, col in self._tokenize(text) ]