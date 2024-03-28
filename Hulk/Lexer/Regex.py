from Hulk.Grammar.gramarlr1 import Gramarlr1

# Get the Hulk Grammar
gramar = Gramarlr1()
# Get the Terminals
s = gramar.Grammar.Get_Terminal
# Get in vars the Terminals
for_exp = s('for')
let = s('let')
if_exp = s('if')
else_exp = s('else')
elif_exp = s('elif')
while_exp = s('while')
function = s('function')
"""
print_exp = s('print')
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
lparen = s('(')
rparen = s(')')
lbrack = s('[')
rbrack = s(']')
lbrace = s('{')
rbrace = s('}')
comma = s(',')
period = s('.')
colon = s(':')
semicolon = s(';')
arrow = s('->')
darrow = s('=>')
and_exp = s('&')
or_exp = s('|')
not_exp = s('!')
modulus = s('%')
power = s('^')
destruct = s(':=')
concat = s('@')
is_exp = s('is')
as_exp = s('as')
"""
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

    (number, "([0..9]+\.)?[0..9]+"),
    (string, "\"((\\\\\")|(\\A))*\"")
]
# Next aft funtion in regex
"""
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
    (lbrack, "\["),
    (rbrack, "\]"),
    (lbrace, "{"),
    (rbrace, "}"),
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
    # (identifier, "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"),
"""

def Get_Hulk_Regex():
    """
    Retorna las Regex del Hulk además del EOF de la gramática
    """
    return Hulk_Regex, gramar.EOF
