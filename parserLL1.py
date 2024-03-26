try:
    from pycompiler import ContainerSet, Grammar, Production, Sentence, EOF
except:
    from tools.pycompiler import ContainerSet, Grammar, Production, Sentence, EOF

def compute_local_first(firsts: dict, alpha):
    '''
    Calcula los firsts de la forma oracional `alpha`, para un conjunto de first actuales

    Parametros
    -----------
        `firsts`: Diccionario de formas oracaionales y firsts
        `alpha`: Forma oracional

    Retorna
    -----------
        `first_alpha`: El conjunto de no terminales obtenidos, dentro de un `ContainerSet`
    '''
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon(True)
    elif alpha[0].IsTerminal:
        first_alpha.add(alpha[0])
    elif alpha[0].IsNonTerminal:
        if len(alpha) > 1:
            first_alpha.update(firsts[alpha[0]])
        else:
            first_alpha.hard_update(firsts[alpha[0]])
        #if len(alpha) > 1 and alpha[0].IsEpsilon:
        if firsts[alpha[0]].contains_epsilon and len(alpha) > 1:            
            Z = alpha[1:]
            first_alpha.hard_update(compute_local_first(firsts,Z))
        
    return first_alpha

def compute_firsts(G: Grammar):
    '''
    Calcula el First de todas las formas oracionales de la gramatica `G`

    Parametros
    ----------
        `G`: La gramatica a la que se le hallara el conjunto First. Debe ser `Grammar`

    Retorna
    --------------
        `firsts`: Diccionario de todos los Firsts por Producciones, No-terminales y Terminales
    '''
    firsts = {}
    change = True
        
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
                
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            first_X = firsts[X]
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
                        
            local_first = compute_local_first(firsts, alpha)            
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    return firsts

def compute_follows(G, firsts):
    '''
    Funcion para calcular el Follow de todos los No-Terminales de la gramatica `G`
    dado el conjunto de todos los Firsts

    Parametros
    -------------
        `G`: La gramatica a la que se le hallara los conjuntos Follows. Debe ser `Grammar`
        `firsts`: Diccionario de todos los Firsts de la gramatica
    
    Retorna
    --------------
        `follows`: Diccionario de todos los Follows por No-Terminales
    '''
    follows = { }
    change = True
    
    #local_firsts = {}

    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]

            for i in range(0, len(alpha)):
                A = alpha[i]
                if A.IsNonTerminal:
                    firsts_Z = ContainerSet()
                    if i < len(alpha)-1:
                        firsts_Z = compute_local_first(firsts, alpha[i+1:])                    
                    change = change or follows[A].update(firsts_Z)
                    if firsts_Z.contains_epsilon or i == len(alpha)-1:
                        change = change or follows[A].update(follow_X)    
    return follows

def compute_first_follows(G):
    '''
    Calcula todos los conjuntos Firsts y Follows de una gramatica

    Parametros:
    -------------
        `G`: La gramatica a la que se le hallara ambos conjuntos. Debe ser `Grammar`

    Retorna:
    -------------
        `firsts`: Diccionario de todos los Firsts por Producciones, No-terminales y Terminales
        `follows`: Diccionario de todos los Follows por No-Terminales
    '''
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)
    return firsts, follows


def build_parsing_table(G, firsts=None, follows=None):
    '''
    Calcula la tabla de parseo LL(1) de una gramatica `G`

    Parametros
    ----------
        `G`: La gramatica a la que se le hallara la tabla LL(1). Debe ser `Grammar`
        `firsts`: Diccionario de todos los Firsts por Producciones, No-terminales y Terminales
        `follows`: Diccionario de todos los Follows por No-Terminales
    Retorna:
    -----------
        `M`: Tabla LL(1) asociada. Si la gramatica no es LL(1), retorna `None`
    '''
    if firsts is None:
        firsts = compute_firsts(G)
    if follows is None:
        follows = compute_follows(G, firsts)

    M = {}
    for production in G.Productions:
        X = production.Left
        alpha = production.Right
        
        firsts_alpha = firsts[alpha]
        follows_X = follows[X]
        for t in firsts_alpha: 
            # Se comprueba que en la tabla LL(1) no haya algo asignado primero
            if M.get((X,t), None) is not None:                
                print(f'La gramatica {G}, no es LL(1)')
                return None
            M[X, t] = [production]

        if G.Epsilon is firsts_alpha or alpha.IsEpsilon:
            for t in follows_X:
                # Se comprueba que en la tabla LL(1) no haya algo asignado primero
                if M.get((X,t), None) is not None:                
                    print(f'La gramatica {G}, no es LL(1)')
                    return None
                M[X, t] = [production]
    return M  


def parser_LL1_generator(G, M=None, firsts=None, follows=None):
    '''
    Generador de parser LL(1)

    Parametros:
    -----------
        `G`: La gramatica a la que se le hallara la tabla LL(1). Debe ser `Grammar`
        `M`: Tabla LL(1) asociada. Si la gramatica no es LL(1)
        `firsts`: Diccionario de todos los Firsts por Producciones, No-terminales y Terminales
        `follows`: Diccionario de todos los Follows por No-Terminales

    Retorna:
    -----------
        `parser`: Parser LL(1) asociado. Funcion que recibe una secuencia de tokens y
        genera la secuencia de producciones que parsea la cadena. Si la gramatica
        no es LL(1) se retorna None.
    '''
        
    if M is None:
        M = build_parsing_table(G=G, firsts=firsts, follows=follows)
        if M is None:
            print('La gramatica no es LL(1)')
            return None
        
    def parser(w):
        stack = [G.startSymbol]
        cursor = 0
        output = []
        
        while len(stack) > 0:
            top = stack.pop()
            a = w[cursor].token_type
            if a == top:                                
                cursor += 1
                if cursor == len(w):
                    break
                else:
                    continue

            production = M[top, a][0]            
            output.append(production)
            for item in reversed(production.Right):
                stack.append(item)            
        
        return output
        
    return parser

def evaluate_parse(left_parse, tokens):
    '''
    Evaluador de gramaticas atributadas.

    Parametros:
    ------------
        `left_parse`: Iterable de las Producciones del parseo realizado
        `tokens`: Iterable de los tokens que generaron la cadena de producciones

    Retorna:
    ------------
        `result`: El resultado de evaluar la gramatica. Este depende de la definicion de sus atributos
    '''
    if not left_parse or not tokens:
        return
    
    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)
    
    assert isinstance(next(tokens).token_type, EOF)
    return result
    

def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes
    
    synteticed = [None] * len(attributes)
    inherited = [None] * len(attributes)
    inherited[0] = inherited_value

    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None            
            token = next(tokens) 
            synteticed[i] = token.lex
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left            
            if attributes[i] is not None:
                inherited[i] = attributes[i](inherited, synteticed)
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited_value=inherited[i])
        
    return attributes[0](inherited, synteticed)