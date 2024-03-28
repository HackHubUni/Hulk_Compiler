from gramarlr1 import Gramarlr1
# Get the Hulk Grammar
gramar = Gramarlr1()
#Get the Terminals
s = gramar.Grammar.Get_Terminal
#Get in vars the Terminals
for_exp = s('for')
let = s('let')
if_exp = s('if')
else_exp= s('else')
elif_exp = s('elif')
while_exp = s('while')
function = s('function')
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


Hulk_Regex = [
    (for_exp, "for"),
    (let, "let"),
    (if_exp, "if"),
    (else_, "else"),
    (elif_, "elif"),
    (while_, "while"),
    (function, "function"),
    (print_, "print"),
    (pi, "pi"),
    (e, "e"),
    (new, "new"),
    (inherits, "inherits"),
    (protocol, "protocol"),
    (type_, "type"),
    (self_, "self"),
    (in_, "in"),
    (range_, "range"),
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
    (and_, "&"),
    (or_, "\|"),
    (not_, "\!"),
    (modulus, "%"),
    (power, "^"),
    (destruct, ":="),
    (concat, "@"),
    (is_, "is"),
    (as_, "as"),
    (identifier, "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"),
    (number, "([0..9]+\.)?[0..9]+"),
    (string, "\"((\\\\\")|(\\A))*\"")
]
