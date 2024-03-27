import json
from typing import Tuple


class Symbol(object):
    """
    Modelaremos los **símbolos** del lenguaje con la clase `Symbol`. Esta clase funcionará como base para la definición de terminales y no terminales. Entre las funcionalidades básicas de los símbolos tenemos que:
    - Pueden ser agrupados con el operador `+` para formar oraciones.
    - Podemos conocer si representa la cadena especial **epsilon** a través de la propiedad `IsEpsilon` que poseen todas las instancias.
    - Podemos acceder a la gramática en la que se definió a través del campo `Grammar` de cada instancia.
    - Podemos consultar la notación del símbolo a través del campo `Name` de cada instancia.

    Los símbolos no deben ser instanciados directamente (ni sus descendiente) con la aplicación de su constructor. En su lugar, utilizaremos una sintaxis descrita más adelante para definirlos junto a la especificación de la gramática.
    """
    Name = None

    """
    
    """
    Grammar = None

    """
    - Podemos acceder a la gramática en la que se definió a través del campo `Grammar` de cada instancia.
    """

    def __init__(self, name, grammar):
        self.Name = name
        """
            - Podemos consultar la notación del símbolo a través del campo `Name` de cada instancia.
        """
        self.Grammar = grammar
        """
           - Podemos acceder a la gramática en la que se definió a través del campo `Grammar` de cada instancia.
        """

    def __str__(self):
        return self.Name

    def __repr__(self):
        return repr(self.Name)

    def __add__(self, other):
        """

        :param other: con el operador `+` podemos concatenar símbolos para formar oraciones.

        """
        if isinstance(other, Symbol):
            return Sentence(self, other)

        raise TypeError(other)

    def __or__(self, other):

        if isinstance(other, (Sentence)):
            return SentenceList(Sentence(self), other)

        raise TypeError(other)

    @property
    def IsEpsilon(self):
        """

        :return: Podemos conocer si representa la cadena especial **epsilon** a través de la propiedad `IsEpsilon` que poseen todas las instancias.
        """
        return False

    def __len__(self):
        return 1


class NonTerminal(Symbol):
    """Los símbolos **no terminales** los modelaremos con la clase `NonTerminal`. Dicha clase extiende la clase `Symbol` para:
    - Añadir noción de las producción que tiene al no terminal como cabecera. Estas pueden ser conocidas a través del campo `productions` de cada instancia.
    - Permitir añadir producciones para ese no terminal a través del operador `%=`.
    - Incluir propiedades `IsNonTerminal` - `IsTerminal` que devolveran `True` - `False` respectivamente.

    Los no terminales no deben ser instanciados directamente con la aplicación de su constructor. En su lugar, se presentan las siguientes facilidades para definir no terminales a partir de una instancia `G` de `Grammar`:
    - Para definir un único no terminal:

        - non_terminal_var = G.NonTerminal('<non-terminal-name>')
        - non_terminal_var    <--- variable en la que guardaremos la referencia al no terminal.
        - <non-terminal-name> <--- nombre concreto del no terminal.

    - Para definir el símbolo distingido:

        - start_var = G.NonTerminal('<start-name>', True)
        - start_var    <--- variable en la que guardaremos la referencia símbolo distinguido.
        - <start-name> <--- nombre concreto del símbolo distinguido.

    - Para definir múltiples no terminales:

        - var1, var2, ..., varN = G.NonTerminals('<name1> <name2> ... <nameN>')
        - var1, var2, ..., varN    <--- variables en las que guardaremos las referencias a los no terminales.
        - <name1> <name2> ... <nameN> <--- nombres concretos del no terminales (separados por espacios).

    """
    productions = []

    def __init__(self, name, grammar):
        super().__init__(name, grammar)
        self.productions = []
        """
        Añadir noción de las producción que tiene al no terminal como cabecera. Estas pueden ser conocidas a través del campo `productions` de cada instancia.
        """

    def __imod__(self, other):
        """
        - Permitir añadir producciones para ese no terminal a través del operador `%=`.

        """
        if isinstance(other, (Sentence)):
            p = Production(self, other)
            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, tuple):
            assert len(other) > 1

            if len(other) == 2:
                other += (None,) * len(other[0])

            assert len(other) == len(
                other[0]) + 2, "Debe definirse una, y solo una, regla por cada símbolo de la producción"
            # assert len(other) == 2, "Tiene que ser una Tupla de 2 elementos (sentence, attribute)"

            if isinstance(other[0], Symbol) or isinstance(other[0], Sentence):
                p = AttributeProduction(self, other[0], other[1:])
            else:
                raise Exception("")

            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, Symbol):
            p = Production(self, Sentence(other))
            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, SentenceList):

            for s in other:
                p = Production(self, s)
                self.Grammar.Add_Production(p)

            return self

        raise TypeError(other)

    @property
    def IsTerminal(self):
        return False

    @property
    def IsNonTerminal(self):
        return True

    @property
    def IsEpsilon(self):
        return False


class Terminal(Symbol):
    """
        Los símbolos **terminales** los modelaremos con la clase `Terminal`. Dicha clase extiende la clase `Symbol` para:
    - Incluir propiedades `IsNonTerminal` - `IsTerminal` que devolveran `True` - `False` respectivamente.

    Los terminales no deben ser instanciados directamente con la aplicación de su constructor. En su lugar, se presentan las siguientes facilidades para definir no terminales a partir de una instancia `G` de `Grammar`:
    - Para definir un único terminal:

        - terminal_var = G.Terminal('<terminal-name>')
        - terminal_var    <--- variable en la que guardaremos la referencia al terminal.
        - <terminal-name> <--- nombre concreto del terminal.

    - Para definir múltiples terminales:

        - var1, var2, ..., varN = G.Terminals('<name1> <name2> ... <nameN>')
        - var1, var2, ..., varN    <--- variables en las que guardaremos las referencias a los terminales.
        - <name1> <name2> ... <nameN> <--- nombres concretos del terminales (separados por espacios).

    """

    def __init__(self, name, grammar):
        super().__init__(name, grammar)

    @property
    def IsTerminal(self):
        return True

    @property
    def IsNonTerminal(self):
        return False

    @property
    def IsEpsilon(self):
        return False


class EOF(Terminal):
    """
    Modelaremos el símbolo de fin de cadena con la clase `EOF`. Dicha clase extiende la clases `Terminal` para heradar su comportamiento.

    La clase `EOF` no deberá ser instanciada directamente con la aplicación de su constructor. En su lugar, una instancia concreta para determinada gramática `G` de `Grammar` se construirá automáticamente y será accesible a través de `G.EOF`.
    """

    def __init__(self, Grammar):
        super().__init__('$', Grammar)


class Sentence(object):
    """
    Modelaremos los **oraciones** y **formas oracionales** del lenguaje con la clase `Sentence`. Esta clase funcionará como una colección de terminales y no terminales. Entre las funcionalidades básicas que provee tenemos que nos :
    - Permite acceder a los símbolos que componen la oración a través del campo `_symbols` de cada instancia.
    - Permite conocer si la oración es completamente vacía a través de la propiedad `IsEpsilon`.
    - Permite obtener la concatenación con un símbolo u otra oración aplicando el operador `+`.
    - Permite conocer la longitud de la oración (cantidad de símbolos que la componen) utilizando la función *build-in* de python `len(...)`.

    Las oraciones pueden ser agrupadas usando el operador `|`. Esto nos será conveniente para definir las producciones las producciones que tengan la misma cabeza (no terminal en la parte izquierda) en una única sentencia. El grupo de oraciones se maneja con la clase `SentenceList`.

    No se deben crear instancias de `Sentence` y `SentenceList` directamente con la aplicación de los respectivos constructores. En su lugar, usaremos el operador `+` entre símbolos para formar las oraciones, y el operador `|` entre oraciones para agruparlas.
    """

    def __init__(self, *args):
        self._symbols = tuple(x for x in args if not x.IsEpsilon)
        self.hash = hash(self._symbols)

    def __len__(self):
        return len(self._symbols)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(*(self._symbols + (other,)))

        if isinstance(other, Sentence):
            return Sentence(*(self._symbols + other._symbols))

        raise TypeError(other)

    def __or__(self, other):
        if isinstance(other, Sentence):
            return SentenceList(self, other)

        if isinstance(other, Symbol):
            return SentenceList(self, Sentence(other))

        raise TypeError(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ("%s " * len(self._symbols) % tuple(self._symbols)).strip()

    def __iter__(self):
        """
        Iterador sobre los simbolos
        :return: los simbolos de la forma oracional
        """
        return iter(self._symbols)

    def __getitem__(self, index):
        return self._symbols[index]

    def __eq__(self, other):
        return self._symbols == other._symbols

    def __hash__(self):
        return self.hash

    @property
    def IsEpsilon(self):
        return False


class SentenceList(object):
    """
    Las oraciones pueden ser agrupadas usando el operador `|`. Esto nos será conveniente para definir las producciones las producciones que tengan la misma cabeza (no terminal en la parte izquierda) en una única sentencia. El grupo de oraciones se maneja con la clase `SentenceList`.

    No se deben crear instancias de `SentenceList` directamente con la aplicación de los respectivos constructores. En su lugar, usaremos el operador `+` entre símbolos para formar las oraciones, y el operador `|` entre oraciones para agruparlas.
    """

    def __init__(self, *args):
        self._sentences = list(args)

    def Add(self, symbol):
        if not symbol and (symbol is None or not symbol.IsEpsilon):
            raise ValueError(symbol)

        self._sentences.append(symbol)

    def __iter__(self):
        return iter(self._sentences)

    def __or__(self, other):
        if isinstance(other, Sentence):
            self.Add(other)
            return self

        if isinstance(other, Symbol):
            return self | Sentence(other)


class Epsilon(Terminal, Sentence):
    """
    Modelaremos tanto la **cadena vacía** como el símbolo que la representa: **epsilon** ($\epsilon$), en la misma clase: `Epsilon`. Dicha clase extiende las clases `Terminal` y `Sentence` por lo que ser comporta como ambas. Sobreescribe la implementación del método `IsEpsilon` para indicar que en efecto toda instancia de la clase reprensenta **epsilon**.

    La clase `Epsilon` no deberá ser instanciada directamente con la aplicación de su constructor. En su lugar, una instancia concreta para determinada gramática `G` de `Grammar` se construirá automáticamente y será accesible a través de `G.Epsilon`.
    """

    def __init__(self, grammar):
        super().__init__('epsilon', grammar)


    def __str__(self):
        return "e"

    def __repr__(self):
        return 'epsilon'

    def __iter__(self):
        yield from ()

    def __len__(self):
        return 0

    def __add__(self, other):
        return other

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))

    def __hash__(self):
        return hash("")

    @property
    def IsEpsilon(self):
        return True


class Production(object):
    """
    Modelaremos las **producciones** con la clase `Production`. Las funcionalidades básicas con que contamos son:

    - Poder acceder la cabecera (parte izquierda) y cuerpo (parte derecha) de cada producción a través de los campos `Left` y `Right` respectivamente.

    - Consultar si la producción es de la forma (X --> epsilon) a través de la propiedad `IsEpsilon`.

    - Desempaquetar la producción en cabecera y cuerpo usando asignaciones: `left, right = production`.

    Las producciones no deben ser instanciadas directamente con la aplicación de su constructor. En su lugar, se presentan las siguientes facilidades para formar producciones a partir de una instancia `G` de `Grammar` y un grupo de terminales y no terminales:
    - Para definir una producción de la forma E x--> E + T:

        E %= E + plus + T

    - Para definir múltiples producciones de la misma cabecera en una única sentencia (E --> E + T | E - T | T):

        E %= E + plus + T | E + minus + T | T

    - Para usar *epsilon* en una producción (ejemplo S --> αS | epsilon) haríamos:

        S %= S + a | G.Epsilon

    """
    Left = None

    Right = None

    def __init__(self, nonTerminal, sentence):

        self.Left = nonTerminal
        """
         Poder acceder la cabecera (parte izquierda) y cuerpo (parte derecha) de cada producción a través de los campos `Left` y `Right` respectivamente.
        """
        self.Right = sentence
        """
         Poder acceder la cabecera (parte izquierda) y cuerpo (parte derecha) de cada producción a través de los campos `Left` y `Right` respectivamente.
        """

    def __str__(self):

        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right

    def __eq__(self, other):
        return isinstance(other, Production) and self.Left == other.Left and self.Right == other.Right

    def __hash__(self):
        return hash((self.Left, self.Right))

    @property
    def IsEpsilon(self):
        """

        :return: Consultar si la producción es de la forma (X --> epsilon) a través de la propiedad `IsEpsilon`.
        """
        return self.Right.IsEpsilon


class AttributeProduction(Production):
    """
    . Cada una de estas producciones se compone por:
    - Un no terminal como cabecera. Accesible a través del campo `Left`.
    - Una oración como cuerpo. Accesible a través del campo `Right`.
    - Un conjunto de reglas para evaluar los atributos. Accesible a través del campo `atributes`.

    Las producciones no deben ser instanciadas directamente con la aplicación de su constructor. En su lugar, se presentan las siguientes facilidades para formar producciones a partir de una instancia
     `G` de `Grammar` y un grupo de terminales y no terminales:
    - Para definir una producción de la forma $B_0 --> B_1 B_2 ... B_n$ que:
        - Asocia a B_0 una regla lambda_0 para sintetizar sus atributos, y
        - Asocia a B_1 .... B_n las reglas lambda_1 .... lambda_n que hereden sus atributos respectivamentes.


    B0 %= B1 + B2 + ... + Bn, lambda0, lambda1, lambda2, ..., lambdaN


    > Donde `lambda0`, `lambda1`, ..., `lambdaN` son funciones que reciben 2 parámetros.
    > 1. Como primer parámetro los atributos heredados que se han computado para cada instancia de símbolo en la producción, durante la aplicación de esa instancia de producción específicamente. Los valores se acceden desde una lista de `n + 1` elementos. Los valores se ordenan según aparecen los símbolos en la producción, comenzando por la cabecera. Nos referiremos a esta colección como `inherited`.
    > 2. Como segundo parámetro los atributos sintetizados que se han computado para cada instancia de símbolo en la producción, durante la aplicación de esa instancia de producción específicamente. Sigue la misma estructura que el primer parámetro. Nos referiremos a esta colección como `synteticed`.
    >
    > La función `lambda0` sintetiza los atributos de la cabecera. La evaluación de dicha función produce el valor de `synteticed[0]`. El resto de los atributos sintetizados de los símbolos de la producción se calcula de la siguiente forma:
    > - En caso de que el símbolo sea un terminal, evalúa como su lexema.
    > - En caso de que el símbolo sea un no terminal, se obtiene de evaluar la función `lambda0` en la instancia de producción correspondiente.
    >
    > La función `lambda_i`, con `i` entre 1 y `n`, computa los atributos heredados de la i-ésima ocurrencia de símbolo en la producción. La evaluación de dicha función produce el valor de `inherited[i]`. El valor de `inherited[0]` se obtiene como el atributo que heredó la instancia concreta del símbolo en la cabecera antes de comenzar a aplicar la producción.
    """
    def __init__(self, nonTerminal:NonTerminal, sentence:Sentence, attributes):
        """
         - Un no terminal como cabecera. Accesible a través del campo `Left`.
         - Una oración como cuerpo. Accesible a través del campo `Right`.
         - Un conjunto de reglas para evaluar los atributos. Accesible a través del campo `atributes`.
        :param nonTerminal: No terminal
        :param sentence: formas oracionales
        :param attributes:
        """
        if not isinstance(sentence, Sentence) and isinstance(sentence, Symbol):
            sentence = Sentence(sentence)
        super(AttributeProduction, self).__init__(nonTerminal, sentence)

        self.attributes = attributes

    def __str__(self):
        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right


    @property
    def IsEpsilon(self):
        return self.Right.IsEpsilon

    # sintetizar en ingles??????, pending aggrement
    def syntetice(self):
        pass


class Grammar():
    """
    Modelaremos las **gramáticas** con la clase `Grammar`. Las funcionalidades básicas con que contamos son:

    - Definir los símbolos _terminales_ y _no terminales_ de la gramática en cuestión a través de los métodos `Terminal` y `Terminals` para los primeros, y `NonTerminal` y `NonTerminals` para los segundos.

    - Definir las producciones de la gramática a partir de la aplicación del operador `%=` entre no terminales y oraciones (estas a su vez formadas por la concatenación de símbolos).

    - Acceder a **todas** las _producciones_ a través del campo `Productions` de cada instancia.

    - Acceder a **todos** los _terminales_ y _no terminales_ a través de los campos `terminals` y `nonTerminals` respectivamente.

    - Acceder al _símbolo distinguido_, _epsilon_ y _fin de cadena_ a través de los campos `startSymbol`, `Epsilon` y `EOF` respectivamente.
    """

    def __init__(self):

        self.Productions = []
        self.nonTerminals = []
        self.terminals = []
        self.startSymbol = None
        # production type
        self.pType = None
        self.Epsilon = Epsilon(self)
        self.EOF = EOF(self)

        self.symbDict = {'$': self.EOF}

    def NonTerminal(self, name: str, startSymbol: bool = False):
        """

        :param name: Nombre del no-terminal a crear
        :param startSymbol: Si el símbolo es el distinguido
        :return: La instancia del no terminal creado
        """
        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = NonTerminal(name, self)

        if startSymbol:

            if self.startSymbol is None:
                self.startSymbol = term
            else:
                raise Exception("Cannot define more than one start symbol.")

        self.nonTerminals.append(term)
        self.symbDict[name] = term
        return term

    def NonTerminals(self, names: str) -> tuple[NonTerminal, ...]:
        """

        :param names: string con los nombres de los no-terminales a crear, separados por espacios
        :return: una tupla de no terminales en el mismo orden que en el string de entrada
        """
        ans = tuple((self.NonTerminal(x) for x in names.strip().split()))

        return ans

    def Add_Production(self, production):

        if len(self.Productions) == 0:
            self.pType = type(production)

        assert type(production) == self.pType, "The Productions most be of only 1 type."

        production.Left.productions.append(production)
        self.Productions.append(production)

    def Terminal(self, name: str):
        """
        Este método crea la instancia del terminal con el nombre dado
        :param name: nombre del terminal
        :return: instancia del terminal creado
        """
        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = Terminal(name, self)
        self.terminals.append(term)
        self.symbDict[name] = term
        return term

    def Terminals(self, names: str):
        """
        Permite crear multiples terminales en una sola linea de codigo
        :param names: String con los nombres de los terminales a crear, separados por espacios
        :return: Los terminales creados en el mismo orden que en el string de entrada
        """
        ans = tuple((self.Terminal(x) for x in names.strip().split()))

        return ans

    def __str__(self):

        mul = '%s, '

        ans = 'Non-Terminals:\n\t'

        nonterminals = mul * (len(self.nonTerminals) - 1) + '%s\n'

        ans += nonterminals % tuple(self.nonTerminals)

        ans += 'Terminals:\n\t'

        terminals = mul * (len(self.terminals) - 1) + '%s\n'

        ans += terminals % tuple(self.terminals)

        ans += 'Productions:\n\t'

        ans += str(self.Productions)

        return ans

    def __getitem__(self, name):
        try:
            return self.symbDict[name]
        except KeyError:
            return None

    @property
    def to_json(self):

        productions = []

        for p in self.Productions:
            head = p.Left.Name

            body = []

            for s in p.Right:
                body.append(s.Name)

            productions.append({'Head': head, 'Body': body})

        d = {'NonTerminals': [symb.Name for symb in self.nonTerminals],
             'Terminals': [symb.Name for symb in self.terminals], \
             'Productions': productions}

        # [{'Head':p.Left.Name, "Body": [s.Name for s in p.Right]} for p in self.Productions]
        return json.dumps(d)

    @staticmethod
    def from_json(data):
        data = json.loads(data)

        G = Grammar()
        dic = {'epsilon': G.Epsilon}

        for term in data['Terminals']:
            dic[term] = G.Terminal(term)

        for noTerm in data['NonTerminals']:
            dic[noTerm] = G.NonTerminal(noTerm)

        for p in data['Productions']:
            head = p['Head']
            dic[head] %= Sentence(*[dic[term] for term in p['Body']])

        return G

    def copy(self):
        G = Grammar()
        G.Productions = self.Productions.copy()
        G.nonTerminals = self.nonTerminals.copy()
        G.terminals = self.terminals.copy()
        G.pType = self.pType
        G.startSymbol = self.startSymbol
        G.Epsilon = self.Epsilon
        G.EOF = self.EOF
        G.symbDict = self.symbDict.copy()

        return G

    @property
    def IsAugmentedGrammar(self):
        augmented = 0
        for left, right in self.Productions:
            if self.startSymbol == left:
                augmented += 1
        if augmented <= 1:
            return True
        else:
            return False

    def AugmentedGrammar(self, force=False):
        if not self.IsAugmentedGrammar or force:

            G = self.copy()
            # S, self.startSymbol, SS = self.startSymbol, None, self.NonTerminal('S\'', True)
            S = G.startSymbol
            G.startSymbol = None
            SS = G.NonTerminal('S\'', True)
            if G.pType is AttributeProduction:
                SS %= S + G.Epsilon, lambda x: x
            else:
                SS %= S + G.Epsilon

            return G
        else:
            return self.copy()
    # endchange


class Item:

    def __init__(self, production, pos, lookaheads=[]):
        self.production = production
        self.pos = pos
        self.lookaheads = frozenset(look for look in lookaheads)

    def __str__(self):
        s = str(self.production.Left) + " -> "
        if len(self.production.Right) > 0:
            for i, c in enumerate(self.production.Right):
                if i == self.pos:
                    s += "."
                s += str(self.production.Right[i])
            if self.pos == len(self.production.Right):
                s += "."
        else:
            s += "."
        s += ", " + str(self.lookaheads)[10:-1]
        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
                (self.pos == other.pos) and
                (self.production == other.production) and
                (set(self.lookaheads) == set(other.lookaheads))
        )

    def __hash__(self):
        return hash((self.production, self.pos, self.lookaheads))

    @property
    def IsReduceItem(self):
        return len(self.production.Right) == self.pos

    @property
    def NextSymbol(self):
        if self.pos < len(self.production.Right):
            return self.production.Right[self.pos]
        else:
            return None

    def NextItem(self):
        if self.pos < len(self.production.Right):
            return Item(self.production, self.pos + 1, self.lookaheads)
        else:
            return None

    def Preview(self, skip=1):
        unseen = self.production.Right[self.pos + skip:]
        return [unseen + (lookahead,) for lookahead in self.lookaheads]

    def Center(self):
        return Item(self.production, self.pos)

class ContainerSet:
    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def extend(self, values):
        change = False
        for value in values:
            change |= self.add(value)
        return change

    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other):
        return self.update(other) | self.epsilon_update(other)

    def find_match(self, match):
        for item in self.set:
            if item == match:
                return item
        return None

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)

    def __nonzero__(self):
        return len(self) > 0

    def __eq__(self, other):
        if isinstance(other, set):
            return self.set == other
        return isinstance(other, ContainerSet) and self.set == other.set and self.contains_epsilon == other.contains_epsilon

class Token:
    """
    Basic token class.

    Parameters
    ----------
    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    """

    def __init__(self, lex, token_type, row=0, col=0):
        self.lex = lex
        self.token_type = token_type
        self.row = row
        self.col = col

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)

    @property
    def is_valid(self):
        return True

class SintacticException(Exception):
    pass