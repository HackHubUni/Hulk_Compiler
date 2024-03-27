from src.Common.Compiler import Grammar
from src.Common.ASTNodes import *

G = Grammar()


# No Terminals
init_ = G.NonTerminal("<init>", startSymbol=True)
program = G.NonTerminal("<program>")
expression = G.NonTerminal("<expression>")
statement = G.NonTerminal("<statement>")
parameters, parameter_list, variable = G.NonTerminals("<parameters> <parameter_list> <variable>")
function_style = G.NonTerminal("<function_style>")
type_def = G.NonTerminal("<type_def>")
protocol_declare, protocol_body = G.NonTerminals("<protocol_declare> <protocol_body>")
simple_expression = G.NonTerminal("<simple_expression>")
expression_block = G.NonTerminal("<expression_block>")
class_block, class_body, class_declaration = G.NonTerminals("<class_block> <class_body> <class_declaration>")
arguments, argument_list = G.NonTerminals("<arguments> <argument_list>")
typed_parameters, typed_parameter_list = G.NonTerminals("<typed_parameters> <typed_parameter_list>")
declaration = G.NonTerminal("<declaration>")
if_block = G.NonTerminal("<if_block>")
else_block = G.NonTerminal("<else_block>")
disjunction, conjunction = G.NonTerminals("<disjunction> <conjunction>")
literal, proposition, boolean = G.NonTerminals("<literal> <proposition> <boolean>")
concatenation = G.NonTerminal("<concatenation>")
arithmetic_expression = G.NonTerminal("<arithmetic_expression>")
module, product, monomial, pow_ = G.NonTerminals("<module> <product> <monomial> <pow>")
high_hierarchy_object, object_exp = G.NonTerminals("<high_hierarchy_object> <object_exp>")
list_ = G.NonTerminal("<list>")

# Terminals
string, identifier, number = G.Terminals("<string> <id> <number>")
plus, minus, times, divide, int_divide = G.Terminals("+ - * / //")
equal, dequal, lesst, greatt, lequal, gequal, notequal = G.Terminals("= == < > <= >= !=")
lparen, rparen, lbrack, rbrack, lbrace, rbrace = G.Terminals("( ) [ ] { }")
comma, period, colon, semicolon = G.Terminals(", . : ;")
arrow, darrow = G.Terminals("-> =>")
and_, or_, not_ = G.Terminals("& | !")

modulus, power, power_asterisk = G.Terminals("% ^ **")
destruct, concat = G.Terminals(":= @")
concat_space = G.Terminal("@@")
list_comprehension = G.Terminal("||")

for_, let, if_, else_, elif_ = G.Terminals("for let if else elif")
while_, function, pi, e, print_ = G.Terminals("while function pi e print")
new, inherits, protocol, type_, self_, in_, range_ = G.Terminals("new inherits protocol type self in range")
true, false = G.Terminals("true false")

extends = G.Terminal("extends")
rand = G.Terminal("rand")
sin, cos, sqrt, exp, log, tan = G.Terminals("sin cos sqrt exp log tan")
as_, is_ = G.Terminals("as is")

init_ %= program, lambda h, s: s[1]

program %= expression, lambda h, s: ProgramNode([], s[1])
program %= statement + program, lambda h, s: ProgramNode([s[1]] + s[2].Statements, s[2].Expression)

statement %= function + identifier + parameters + function_style, lambda h, s: FunctionNode(s[2], s[3], s[4])
statement %= type_ + identifier + type_def, lambda h, s: TypeNode(s[2], s[3].Corpus, s[3].ConstructorParameters, s[3].inherits, s[3].Arguments) # duda
statement %= protocol_declare, lambda h, s: s[1]
#
function_style %= darrow + simple_expression + semicolon, lambda h, s: s[2]
function_style %= colon + identifier + darrow + simple_expression + semicolon, lambda h, s: s[4]
function_style %= lbrace + expression_block + rbrace, lambda h, s: s[2]
function_style %= colon + identifier + lbrace + expression_block + rbrace, lambda h, s: s[4]
#
parameters %= lparen + rparen, lambda h, s: []
parameters %= lparen + parameter_list + rparen, lambda h, s: s[2]
#
parameter_list %= variable, lambda h, s: s[1]
parameter_list %= variable + comma + parameter_list, lambda h, s: [s[1]] + s[3]
#
variable %= identifier, lambda h, s: ParameterNode(s[1])
variable %= identifier + colon + identifier, lambda h, s: ParameterNode(s[1], s[3])
#
type_def %= class_block, lambda h, s: s[1]
type_def %= inherits + identifier + class_block, lambda h, s: s[3]
type_def %= lparen + parameter_list + rparen + class_block, lambda h, s: s[2] + s[4]
type_def %= lparen + parameter_list + rparen + inherits + identifier + class_block, lambda h, s: s[2] + s[6]
type_def %= lparen + parameter_list + rparen + inherits + identifier + lparen + argument_list + rparen + class_block, lambda h, s: s[2] + s[7] + s[9]
type_def %= inherits + identifier + lparen + argument_list + rparen + class_block, lambda h, s: s[4] + s[6]
#
class_block %= lbrack + rbrack, lambda h, s: []
class_block %= lbrack + class_body + rbrack, lambda h, s: s[2]
#
class_body %= class_declaration, lambda h, s: s[1]
class_body %= class_declaration + class_body, lambda h, s: s[1] + s[2]
#
class_declaration %= variable + equal + simple_expression + semicolon, lambda h, s: ClassAtributeNode(s[1], s[3])
class_declaration %= function_style, lambda h, s: s[1]
#
protocol_declare %= protocol + identifier + lbrack + protocol_body + rbrack, lambda h, s: ProtocolNode(s[2], s[4])
protocol_declare %= protocol + identifier + extends + identifier + lbrack + protocol_body + rbrack, lambda h, s: ProtocolNode(s[2], s[6], s[4])
#
protocol_body %= identifier + typed_parameters + colon + identifier + semicolon, lambda h, s: ProtocolMethodNode(s[1], s[2], s[4])
protocol_body %= identifier + typed_parameters + colon + identifier + semicolon + protocol_body, lambda h, s: [ProtocolMethodNode(s[1], s[2], s[3])] + s[6]
#
typed_parameters %= lparen + rparen, lambda h, s: []
typed_parameters %= lparen + typed_parameter_list + rparen, lambda h, s: s[2]
#
typed_parameter_list %= identifier + colon + identifier, lambda h, s: ParameterNode(s[1], s[2])
typed_parameter_list %= identifier + colon + identifier + typed_parameter_list, lambda h, s: [ParameterNode(s[1], s[2])] + s[4]
#
expression %= simple_expression + semicolon, lambda h, s: s[1]
expression %= lbrace + expression_block + rbrace, lambda h, s: s[2]
#
expression_block %= expression, lambda h, s: s[1]
expression_block %= expression_block + expression, lambda h, s: s[1] + s[2]
#
simple_expression %= let + declaration + in_ + expression, lambda h, s: LetNode(s[2].variables, s[2].variables_values, s[3])
simple_expression %= identifier + destruct + simple_expression, lambda h, s: DestructiveExpression(s[1], s[3])
simple_expression %= if_ + if_block + else_block, lambda h, s: s[2] + s[3]
simple_expression %= while_ + lparen + simple_expression + rparen + expression, lambda h, s: whileNode(s[3], s[5])
simple_expression %= for_ + lparen + identifier + in_ + simple_expression + rparen + expression, lambda h, s: forNode(s[3], s[5], s[7])
simple_expression %= new + identifier + arguments, lambda h, s: NewNode(s[2], s[3])
simple_expression %= disjunction, lambda h, s: s[1]
#
declaration %= variable + equal + simple_expression, lambda h, s: LetNode(s[1], s[3], s[0].Expression) # duda
declaration %= variable + equal + simple_expression + comma + declaration, lambda h, s: [LetNode(s[1], s[3], s[0].Expression)] + s[5] # duda
#
if_block %= lparen + simple_expression + rparen + simple_expression, lambda h, s: IfElseExpression(s[2], s[4])
if_block %= lparen + simple_expression + rparen + lbrace + expression_block + rbrace, lambda h, s: IfElseExpression(s[2], s[5])
#
else_block %= else_ + expression, lambda h, s: s[2]
else_block %= elif_ + if_block + else_block, lambda h, s: s[2] + s[3]
#
arguments %= lparen + rparen, lambda h, s: []
arguments %= lparen + argument_list + rparen, lambda h, s: s[2]
#
argument_list %= simple_expression, lambda h, s: s[1]
argument_list %= simple_expression + comma + argument_list, lambda h, s: [s[1]] + s[3]
#
disjunction %= conjunction, lambda h, s: s[1]
disjunction %= conjunction + or_ + disjunction, lambda h, s: OrAndExpression(s[2], s[1], s[3])
#
conjunction %= literal, lambda h, s: s[1]
conjunction %= literal + and_ + conjunction, lambda h, s: OrAndExpression(s[2], s[1], s[3])
#
literal %= proposition, lambda h, s: s[1]
literal %= not_ + literal, lambda h, s: NotExpression(s[2])
#
proposition %= boolean, lambda h, s: s[1]
proposition %= proposition + is_ + identifier, lambda h, s: IsExpression(s[1], s[3])
#
boolean %= concatenation, lambda h, s: s[1]
boolean %= boolean + dequal + concatenation, lambda h, s: ComparationExpression(s[2], s[1], s[3])
boolean %= boolean + notequal + concatenation, lambda h, s: ComparationExpression(s[2], s[1], s[3])
boolean %= boolean + lequal + concatenation, lambda h, s: ComparationExpression(s[2], s[1], s[3])
boolean %= boolean + gequal + concatenation, lambda h, s: ComparationExpression(s[2], s[1], s[3])
boolean %= boolean + lesst + concatenation, lambda h, s: ComparationExpression(s[2], s[1], s[3])
boolean %= boolean + greatt + concatenation, lambda h, s: ComparationExpression(s[2], s[1], s[3])
#
concatenation %= arithmetic_expression, lambda h, s: s[1]
concatenation %= arithmetic_expression + concat + concatenation, lambda h, s: StringConcatenationNode(s[1], s[3])
concatenation %= arithmetic_expression + concat_space + concatenation, lambda h, s: StringConcatenationNode(s[1], s[3], True)
#

arithmetic_expression %= module, lambda h, s: s[1]
arithmetic_expression %= arithmetic_expression + plus + module, lambda h, s: AritmethicExpression(s[2], s[1], s[3])
arithmetic_expression %= arithmetic_expression + minus + module, lambda h, s: AritmethicExpression(s[2], s[1], s[3])

module %= product, lambda h, s: s[1]
module %= module + modulus + product, lambda h, s: AritmethicExpression(s[2], s[1], s[3])
#
product %= monomial, lambda h, s: s[1]
product %= product + times + monomial, lambda h, s: AritmethicExpression(s[2], s[1], s[3])
product %= product + divide + monomial, lambda h, s: AritmethicExpression(s[2], s[1], s[3])
product %= product + int_divide + monomial, lambda h, s: AritmethicExpression(s[2], s[1], s[3])
#
monomial %= pow_, lambda h, s: s[1]
monomial %= minus + monomial, lambda h, s: AritmethicExpression(s[1], NumberNode(0), s[2])
#
pow_ %= high_hierarchy_object, lambda h, s: s[1]
pow_ %= pow_ + power_asterisk + high_hierarchy_object, lambda h, s: AritmethicExpression(s[2], s[1], s[3])
pow_ %= pow_ + power + high_hierarchy_object, lambda h, s: AritmethicExpression(s[2], s[1], s[3])
#
high_hierarchy_object %= object_exp, lambda h, s: s[1]
high_hierarchy_object %= high_hierarchy_object + as_ + object_exp, lambda h, s: asNode(s[1], s[3])
#
object_exp %= lparen + simple_expression + rparen, lambda h, s: s[2]
object_exp %= number, lambda h, s: NumberNode(s[1])
object_exp %= string, lambda h, s: StringNode(s[1])
object_exp %= true, lambda h, s: BooleanNode(s[1])
object_exp %= false, lambda h, s: BooleanNode(s[1])
object_exp %= identifier, lambda h, s: s[1]
object_exp %= identifier + arguments, lambda h, s: FunctionCallNode(s[1], s[2])
object_exp %= object_exp + period + identifier, lambda h, s: ClassAtributeCallNode(s[1], s[3])
object_exp %= object_exp + period + identifier + arguments, lambda h, s: ClassFunctionCallNode(s[1], s[3], s[4])
object_exp %= lbrack + list_ + rbrack, lambda h, s: s[2]
object_exp %= object_exp + lbrack + simple_expression + rbrack, lambda h, s: InexingNode(s[1], s[3])
object_exp %= print_ + lparen + simple_expression + rparen, lambda h, s: FunctionCallNode(s[1], s[3])
object_exp %= sin + lparen + simple_expression + rparen, lambda h, s: FunctionCallNode(s[1], s[3])
object_exp %= cos + lparen + simple_expression + rparen, lambda h, s: FunctionCallNode(s[1], s[3])
object_exp %= tan + lparen + simple_expression + rparen, lambda h, s: FunctionCallNode(s[1], s[3])
object_exp %= sqrt + lparen + simple_expression + rparen, lambda h, s: FunctionCallNode(s[1], s[3])
object_exp %= exp + lparen + simple_expression + rparen, lambda h, s: FunctionCallNode(s[1], s[3])
object_exp %= log + lparen + simple_expression + comma + simple_expression + rparen, lambda h, s: FunctionCallNode(s[1], s[3] + s[5]) # duda
object_exp %= rand + lparen + rparen, lambda h, s: FunctionCallNode(s[1], [])
#
list_ %= simple_expression, lambda h, s: s[1]
list_ %= simple_expression + comma + list_, lambda h, s: ListNode([s[1]] + s[3]) # duda
list_ %= simple_expression + list_comprehension + identifier + in_ + simple_expression, lambda h, s: ImplicitListNode(s[1], s[3], s[5])


def GetKeywords():
    return [for_, let, if_, else_, elif_, while_, function, pi, e, print_,
            new, inherits, protocol, type_, self_, in_, range_, true, false, extends, as_,
            rand, sin, cos, sqrt, exp, log, is_, tan]