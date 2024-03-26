try:
    from automata import NFA, automata_union, automata_concatenation, automata_closure, automata_positive_closure, nfa_to_dfa
    from pycompiler import Grammar, Token
    from parserLL1 import parser_LL1_generator, evaluate_parse
except:
    from tools.automata import NFA, automata_union, automata_concatenation, automata_closure, automata_positive_closure, nfa_to_dfa
    from tools.pycompiler import Grammar, Token
    from tools.parserLL1 import parser_LL1_generator, evaluate_parse
########## Clases Base para los nodos del AST ##########

class Node:
    def evaluate(self):
        raise NotImplementedError()
        
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node
        
    def evaluate(self):
        value = self.node.evaluate() 
        return self.operate(value)
    
    @staticmethod
    def operate(value):
        raise NotImplementedError()
        
class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def evaluate(self):
        lvalue = self.left.evaluate() 
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

######### Nodos Automata AST ############

EPSILON = 'ε'

class EpsilonNode(AtomicNode):
    def evaluate(self):   
        nfa = NFA(states=2,
            finals=[1],
            transitions={
                (0, ''): [1],
            },
            start=0)
        return nfa

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        nfa = NFA(states=2,
            finals=[1],
            transitions={
                (0, s): [1],
            },
            start=0)
        return nfa   

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        closure = automata_closure(value)
        #closure.graph().write_png('closure.png')
        return closure

class PositiveClosureNode(UnaryNode):
    @staticmethod
    def operate(value):                
        closure = automata_positive_closure(value)
        return closure

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):                
        union = automata_union(lvalue, rvalue)
        #union.graph().write_png('union.png')
        return union

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):        
        concat = automata_concatenation(lvalue, rvalue)
        #concat.graph().write_png('concat.png')
        return concat

############### Gramatica de REGEX ####################

def GrammarRegexSimple():
    '''
    Generador de la gramatica LL(1) para expresiones regulares simples
    Solo implementa Union, Concatenacion y Clausura
    
    La gramatica es:

    E   -> TX
    X   -> |E
        -> epsilon
    T   -> FY
    Y   -> T
        -> epsilon
    F   -> AZ
    Z   -> *
        -> epsilon
    A   -> t
        -> (E)
        -> ε

    Retorna:
    --------------
    `G`: Gramatica REGEX Simple (instancia de `Grammer`)
    '''
    G = Grammar()

    E = G.NonTerminal('E', True)
    T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
    pipe, star, opar, cpar, symbol, epsilon, plus = G.Terminals('| * ( ) symbol ε +')

    G._fixed_tokens = {
        '*': Token('*', star),
        '+': Token('+', plus),
        '|': Token('|', pipe),
        '(': Token('(', opar),
        ')': Token(')', cpar),
        'ε': Token('ε', epsilon),
    }
    G._symbol = symbol

    E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]

    X %= pipe + E, lambda h,s: UnionNode(h[0], s[2]), None, None
    X %= G.Epsilon, lambda h,s: h[0]#, None

    T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]

    Y %= T, lambda h, s: ConcatNode(h[0], s[1]), None
    Y %= G.Epsilon, lambda h,s: h[0]#, None

    F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]

    Z %= star, lambda h,s: ClosureNode(h[0]), None
    Z %= plus, lambda h,s: PositiveClosureNode(h[0]), None
    Z %= G.Epsilon, lambda h,s: h[0]

    A %= symbol, lambda h,s: SymbolNode(s[1]), None
    A %= opar + E + cpar, lambda h,s: s[2], None, None, None
    A %= epsilon, lambda h,s: EpsilonNode(EPSILON), None

    return G

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []

    force_symbol = False
    fixed_tokens = G._fixed_tokens
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        if not force_symbol and char == '\\':
            force_symbol = True
            continue
        token = fixed_tokens.get(char, None)
        if token is None or force_symbol:
            token =  Token(char, G._symbol)
            force_symbol = False
        tokens.append(token)

    tokens.append(Token('$', G.EOF))
    return tokens

class RegexSimple():
    def __init__(self, regular_exp, skip_whitespaces= False) -> None:
        self.exregular_expp = regular_exp
        self._grammer = GrammarRegexSimple()
        self._parser = parser_LL1_generator(self._grammer)
        self._tokens = regex_tokenizer(regular_exp, self._grammer, skip_whitespaces=skip_whitespaces)
        self._left_parse = self._parser(self._tokens)
        self._ast = evaluate_parse(self._left_parse, self._tokens)
        self._nfa = self._ast.evaluate()
        #self._nfa.graph().write_png('nfa.png')
        self._dfa = nfa_to_dfa(self._nfa)
        #self._dfa.graph().write_png('dfa.png')

    def recognize(self, text):
        return self._dfa.recognize(text)

    def automaton(self):
        return self._dfa
