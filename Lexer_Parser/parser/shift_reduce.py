
from Lexer_Parser.utils.automata import State
from cmp.pycompiler import Grammar, Item, ContainerSet, EOF, SintacticException,Token
from Lexer_Parser.utils.parserLL1 import compute_firsts, compute_follows, compute_local_first

try:
    from pandas import DataFrame
except:
    pass

def build_LR0_automaton(G: Grammar):
    '''
    Construye un automata LR0 a partir de una gramatica. El automata creado
    con esta funcion es la version No Determinista. Se recomienda hacerle
    la transformacion a un DFA para su uso. La gramatica debe estar aumentada,
    si el distinguido tiene varias producciones.

    Parametros:
    --------------
        `G`: Gramatica a la que se le quiere construir el automata. Debe ser instancia de `Grammar`,
        y ser una gramatica aumentada.
    '''
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [ start_item ]
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue
                
        kernel = Item(current_item.production, current_item.pos + 1)
        kernel_state = State(kernel, True)
        visited[kernel] = kernel_state

        next_symbol = current_item.NextSymbol
        no_kernels = []
        if next_symbol.IsNonTerminal:
            for production in next_symbol.productions:
                no_kernel = Item(production, 0)
                if no_kernel not in visited.keys():
                    visited[no_kernel] = State(no_kernel, True)
                    pending.append(no_kernel)
                no_kernels.append(no_kernel)
        
        current_state = visited[current_item]        
                
        current_state.add_transition(next_symbol.Name, visited[kernel])
        pending.append(kernel)
        for no_kernel in no_kernels:
            current_state.add_epsilon_transition(visited[no_kernel])            

    return automaton

class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G: Grammar, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, f'Shift-Reduce or Reduce-Reduce conflict!!! se quiere poner{key } en la tabla pero esta {value}'
        table[key] = value

    def __call__(self, w:list[Token]):
        """
        A method to parse a given list of tokens using a shift-reduce parser.
        It takes a list of tokens 'w' as input.
        Returns the parsed output and the sequence of operations performed.
        """

        stack = [ 0 ]
        cursor = 0
        output = []
        operations = []
        oper=[]
        count= 1
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:], count)
            count+=1
                            
            lookahead = lookahead.token_type.Name
            if (state, lookahead) not in self.action.keys():
                ##########################TODO###########################
                # Mejorar la informacion al detectar error en la cadena #
                #########################################################
                desire = ''
                for (state_d, lookahead_d) in self.action.keys():
                    if state_d == state:
                        desire += f"- '{lookahead_d}'\n"

                token = w[cursor]
                err = f'No se puede parsear la cadena. No se esperaba un token {lookahead} '
                err += f'en la linea {token.row} y columna {token.col}.\n'
                err += f'El token actual es {token.lex}\n'
                err += f'Los tokens restantes son: {w[cursor:]}\n'
                err += f'El estado actual es {state}\n'
                err += f'El estado actual de las derivaciones es {output}'

                if len(desire) > 0:
                    err += 'Se esperaba:\n'
                    err +=  desire
                raise SintacticException(err)
            
            action, tag = self.action[state, lookahead]
            
            # SHIFT
            if action == ShiftReduceParser.SHIFT:
                stack.append(lookahead)
                stack.append(tag)
                operations.append(ShiftReduceParser.SHIFT)
                cursor += 1

            # REDUCE
            elif action == ShiftReduceParser.REDUCE:
                left, right = production = self.G.Productions[tag]
                count_delete = 2 * len(right)
                for i in range(count_delete):
                    stack.pop()
                new_state = self.goto[stack[-1], left.Name]
                stack.append(left.Name)
                stack.append(new_state)
                output.append(production)
                operations.append(ShiftReduceParser.REDUCE)

            # ACCEPT
            elif action == ShiftReduceParser.OK:
                return output, operations

            # INVALID 
            else:
                raise Exception('Invalid')

class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state                

                if not item.IsReduceItem:
                    symbol =  item.NextSymbol
                    if symbol.IsTerminal:                        
                        node_transition = node.transitions.get(symbol.Name, None)
                        if node_transition is not None:
                            assert len(node_transition) == 1, 'Automata No Determinista.'
                            self._register(self.action,
                                        (idx, item.NextSymbol.Name),
                                        (ShiftReduceParser.SHIFT, node_transition[0].idx))
                    else:
                        node_transition = node.transitions.get(symbol.Name, None)
                        if node_transition is not None:
                            assert len(node_transition) == 1, 'Automata no determinista.'
                            self._register(self.goto,
                                        (idx, item.NextSymbol.Name),
                                        (node_transition[0].idx))                    
                else:
                    left, right = production = item.production
                    k = G.Productions.index(production)
                    if left.Name == G.startSymbol.Name:
                        k = G.Productions.index(item.production)
                        self._register(self.action,
                            (idx, G.EOF.Name),
                            (ShiftReduceParser.OK, k))                    
                    for terminal in follows[left]:
                        ################TODO##############
                        # Mejorar la actualizacion de OK #
                        ##################################
                        if terminal == G.EOF and left.Name == G.startSymbol.Name:
                            continue
                        self._register(self.action,
                                    (idx, terminal.Name),
                                    (ShiftReduceParser.REDUCE, k))

def expand(item, firsts):
    '''
    Esta recibe un item LR(1) y devuelve el conjunto de items
    que sugiere incluir (directamente) debido a la presencia de un `.`
    delante de un no terminal.
    
    Parametros
    --------------
        `item`: Item LR(1) a expandir
        `firsts`: El conjunto de firsts

    Retorna:
    --------------
        `lookaheads`: El conjunto de las producciones sugeridas,
        con los lookaheads que pertenecen al Firsts del resto de la
        formal oracional y su lookahead actual
    '''
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
     
    for preview in item.Preview():
        local_firsts= compute_local_first(firsts, preview)
        for production in next_symbol.productions:
            new_item = Item(production, 0, local_firsts)
            lookaheads.add(new_item)
    
    assert not lookaheads.contains_epsilon
    
    return list(lookaheads)

def compress(items):
    '''
    Dado un conjunto de items LR(1) comprime aquellos con el mismo centro,
    dejando el lookhead como una lista de la union de cada lookahead

    Parametros:
    ----------
        `items`: Iterable de `Item` (representaciones de Items LR(1))
    
    Retorna:
    --------
        `items_compress`: Lista de Items ya comprimidos
    '''

    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

def closure_lr1(items, firsts):
    '''
    Computa la clausura de un conjunto LR(1). Esta clausura se va formando
    recursivamente con la expansion de los items LR(1), cuyo simbolo despues
    de `.` es un No Terminal.

    Parametros:
    ------------
        `items`: Items LR(1)
        `firsts`: Coleccion de los Firsts de la Gramatica

    Retorna:
    ------------
        `closure`: Colecci'on de items resultantes comprimidos
    '''
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        
        for item in closure:
            if not item.IsReduceItem and item.NextSymbol.IsNonTerminal:
                exp = expand(item, firsts)
                new_items.extend(exp)

        changed = closure.update(new_items)
        
    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    '''
    La función recibe como parámetro un conjunto de items y un símbolo,
    y devuelve el conjunto `goto(items, symbol)`, es decir la coleccion
    de items a los que se puede acceder desde alguno de los itmes actuales
    utilizando `symbol` como transicion.

    Parametros
    -----------
        `items`: Conjunto de Items LR(1)
        `symbol`: Simbolo por el que se quiere realizar la transicion
        `firsts`: Firsts de la gramatica. Solo especificarlo si `just_kernel=True`
        `just_kernel`: Para calcular solamente el conjunto de items kernels
    
    Retorna
    ----------
        `new_items`: Conjunto de Items a los que se puede llegar mediante el simbolo
    '''

    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

def build_LR1_automaton(G):
    '''
    Construye un Automata LR(1) (directamente se construye determinista).
    Reconoce todos los prefijos viables de la Gramatica.
    La Gramatica proporcionada debe tener el distinguido con una sola produccion.

    Parametros:
    ------------
        `G`: Gramatica Aumentada

    Retorna:
    -----------
        `automaton`: Automata Determinista LR(1)
    '''

    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]
        
        for symbol in G.terminals + G.nonTerminals:
                       
            goto = frozenset(goto_lr1(current_state.state, symbol, firsts))
            if len(goto) == 0:
                continue
            if goto not in visited.keys():
                next_state = State(goto, True)
                visited[goto] = next_state
                pending.append(goto)
            else:
                next_state = visited[goto]
            
            current_state.add_transition(symbol.Name, next_state)
        
    return automaton

class LR1Parser(ShiftReduceParser):
    '''
    Parser LR(1) Shift-Reduce
    '''

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:

                if not item.IsReduceItem:
                    symbol =  item.NextSymbol
                    if symbol.IsTerminal:                        
                        node_transition = node.transitions.get(symbol.Name, None)
                        if node_transition is not None:
                            assert len(node_transition) == 1, 'Automata No Determinista.'
                            self._register(self.action,
                                        (idx, item.NextSymbol.Name),
                                        (ShiftReduceParser.SHIFT, node_transition[0].idx))
                    else:
                        node_transition = node.transitions.get(symbol.Name, None)
                        if node_transition is not None:
                            assert len(node_transition) == 1, 'Automata no determinista.'
                            self._register(self.goto,
                                        (idx, item.NextSymbol.Name),
                                        (node_transition[0].idx))                    
                else:
                    left, right = production = item.production
                    k = G.Productions.index(production)
                    if left.Name == G.startSymbol.Name:
                        k = G.Productions.index(item.production)
                        self._register(self.action,
                            (idx, G.EOF.Name),
                            (ShiftReduceParser.OK, k))                    
                    for terminal in item.lookaheads:
                        ################TODO##############
                        # Mejorar la actualizacion de OK #
                        ##################################
                        if terminal == G.EOF and left.Name == G.startSymbol.Name:
                            continue
                        self._register(self.action,
                                    (idx, terminal.Name),
                                    (ShiftReduceParser.REDUCE, k))

def evaluate_reverse_parse(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token.lex)
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(rule is None for rule in attributes[1:]), 'There must be only synteticed attributes.'
            rule = attributes[0]

            if len(body):
                synteticed = [None] + stack[-len(body):]
                value = rule(None, synteticed)
                stack[-len(body):] = [value]
            else:
                stack.append(rule(None, None))
        else:
            raise Exception('Invalid action!!!')

    assert len(stack) == 1
    assert isinstance(next(tokens).token_type, EOF)
    return stack[0]

def encode_value(value):
    try:
        action, tag = value
        if action == ShiftReduceParser.SHIFT:
            return 'S' + str(tag)
        elif action == ShiftReduceParser.REDUCE:
            return repr(tag)
        elif action ==  ShiftReduceParser.OK:
            return action
        else:
            return value
    except TypeError:
        return value

def table_to_dataframe(table):
    d = {}
    for (state, symbol), value in table.items():
        value = encode_value(value)
        try:
            d[state][symbol] = value
        except KeyError:
            d[state] = { symbol: value }

    return DataFrame.from_dict(d, orient='index', dtype=str)
