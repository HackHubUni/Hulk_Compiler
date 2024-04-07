from Hulk.Semantic_Check.basic_types.Object_Type import Object
from Hulk.tools.Ast import *

plus=FunctionDeclarationNode('plus', args=[VarDefNode('a', 'Number'), VarDefNode('b', 'Number')], body=PlusNode(),return_type='Number')
minus=FunctionDeclarationNode('minus', args=[VarDefNode('a', 'Number'), VarDefNode('b', 'Number')], body=MinusNode(),return_type='Number')
star=FunctionDeclarationNode('star', args=[VarDefNode('a', 'Number'), VarDefNode('b', 'Number')], body=StarNode(),return_type='Number')
div=FunctionDeclarationNode('div', args=[VarDefNode('a', 'Number'), VarDefNode('b', 'Number')], body=DivNode(),return_type='Number')
power=FunctionDeclarationNode('power', args=[VarDefNode('a', 'Number'), VarDefNode('b', 'Number')], body=PowerNode(),return_type='Number')

TypeDeclarationNode('Number', features=[AssignNode('value', LiteralNumNode()),PlusNode()], args=[VarDefNode('value', 'Number')])


