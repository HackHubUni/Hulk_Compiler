from Hulk.Grammar.gramarlr1 import Gramarlr1
from cmp.pycompiler import Terminal

# Get the Hulk Grammar
gramar = Gramarlr1()
# Get the Terminals
s = gramar.Grammar.Get_Terminal

# the result
regex_list: [(Terminal, str)] = []
# Get in vars the Terminals
#for
for_exp = s('for')
regex_list.append((for_exp, "for"))
#let
let = s('let')
regex_list.append((let, "let"))
#if
if_exp = s('if')
regex_list.append((if_exp, "if"))
#else
else_exp = s('else')
regex_list.append((else_exp, "else"))
#elif
elif_exp = s('elif')
regex_list.append((elif_exp, "elif"))
while_exp = s('while')
regex_list.append((while_exp, "while"))
#function
function = s('function')
regex_list.append((function, "function"))
#Print
print_exp = s('print')
regex_list.append((print_exp, "print"))
pi = s('pi')
e = s('e')
new = s('new')
inherits = s('inherits')
protocol = s('protocol')
type_exp = s('type')
self_exp = s('self')
in_exp = s('in')
range_exp = s('range')
true = s('true')
false = s('false')
extends = s('extends')
sin = s('sin')
cos = s('cos')
tan = s('tan')
sqrt = s('sqrt')
exp = s('exp')
log = s('log')
rand = s('rand')
plus = s('+')
times = s('*')
minus = s('-')
divide = s('/')
equal = s('=')
dequal = s('==')
lesst = s('<')
greatt = s('>')
lequal = s('<=')
gequal = s('>=')

#o_par
lparen = s('(')
regex_list.append((lparen, "("))
# c_par
rparen = s(')')
regex_list.append((rparen, ")"))

#square_o
lbrack = s('[')
regex_list.append((lbrack, "["))

#square_c
rbrack = s(']')
regex_list.append((rbrack, "]"))

# curly_o
lbrace = s('{')
regex_list.append((lbrace, "{"))

# curly_c
rbrace = s('}')
regex_list.append((rbrace, "}"))

#comma
comma = s(',')
regex_list.append((comma, ","))

period = s('.')

#colon
colon = s(':')
regex_list.append((colon, ":"))

#semicolon
semicolon = s(';')
regex_list.append((semicolon, ";"))

arrow = s('->')

#rarrow
darrow = s('=>')
regex_list.append((darrow, "=>"))

#given
given = s('||')
regex_list.append((given, "||"))

and_exp = s('&')
or_exp = s('|')
not_exp = s('!')
modulus = s('%')
power = s('^')
destruct = s(':=')
concat = s('@')
is_exp = s('is')
as_exp = s('as')
identifier = s("identifier")
number = s("numbers")
string = s("string")






###############
# Hulk Regex  #
###############
Hulk_Regex = [
    (for_exp, "for"),
    (let, "let"),
    (if_exp, "if"),
    (else_exp, "else"),
    (elif_exp, "elif"),
    (while_exp, "while"),
    (function, "function"),
    (print_exp, "print"),
    (pi, "pi"),
    (e, "e"),
    (new, "new"),
    (inherits, "inherits"),
    (protocol, "protocol"),
    (type_exp, "type"),
    (self_exp, "self"),
    (in_exp, "in"),
    (range_exp, "range"),
    (true, "true"),
    (false, "false"),
    (extends, "extends"),
    (sin, "sin"),
    (cos, "cos"),
    (tan, "tan"),
    (sqrt, "sqrt"),
    (exp, "exp"),
    (log, "log"),
    (rand, "rand"),
    (plus, "\+"),
    (times, "\*"),
    (minus, "-"),
    (divide, "/"),
    (equal, "="),
    (dequal, "=="),
    (lesst, "<"),
    (greatt, ">"),
    (lequal, "<="),
    (gequal, ">="),
    (lparen, "\("),
    (rparen, "\)"),
    (lbrack, "\["),  #
    (rbrack, "\]"),  #
    (lbrace, "{"),  #
    (rbrace, "}"),  #
    (comma, ","),
    (period, "\."),
    (colon, ":"),
    (semicolon, ";"),
    (arrow, "->"),
    (darrow, "=>"),
    (and_exp, "&"),
    (or_exp, "\|"),
    (not_exp, "\!"),
    (modulus, "%"),
    (power, "^"),
    (destruct, ":="),
    (concat, "@"),
    (is_exp, "is"),
    (as_exp, "as"),
    (identifier, "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"),
    (number, "([0..9]+\.)?[0..9]+"),
    (string, "\"((\\\\\")|(\\A))*\"")
]


# Next aft funtion in regex


def Get_Hulk_Regex():
    """
    Retorna las Regex del Hulk además del EOF de la gramática
    """
    return Hulk_Regex, gramar.EOF
