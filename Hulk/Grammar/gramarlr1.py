from cmp.pycompiler import *  # Gramar Terminal NonTerminal Token
from Hulk.tools.Ast import *


class Gramarlr1:
    def __init__(self) -> None:
        G = Grammar()
        self.Grammar = G
        self.EOF = self.Grammar.EOF

        Program = G.NonTerminal('Program', True)
        #Declaraciones y expresiones
        Declaration_List, Declaration, Statment, Expresion, Simple_Expresion = G.NonTerminals('DeclList Decl Stat Expr SimpleExpr')

        Arithmethic_expression, Disjoin, Conj, Negation, Dyn_Test, Comp, Number_Expression,Term, Factor, Sign, Atomic = G.NonTerminals(
            'ArithExpr Disj Conj Neg DynTest Comp NumExpr Term Factor Sign Atom')
        
        Attr_Call, Closed_Expression, Function_Call, Method_Call, Method_Call_List = G.NonTerminals('Attr_Call Closed_Expression Function_Call Method_Call Method_Call_List')

        ExprBlock, StatList, Expression_List, Expression_Trail, Assigment_List, Var_Declaration, Elif_Branch = G.NonTerminals(
            'ExprBlock StatList ExprList ExprTail AssignList VarDecl ElifBranch')

        Func_Declaration, Body, Argument_List, Arg_Tail, Type_Declaration, Feature_List = G.NonTerminals(
            'FuncDecl Body ArgList ArgTail TypeDecl FeatureList')

        Protocol_Declaration, Protocol_Methods, Full_Type_Arguments, Fully_Typed_Tail, Type_List = G.NonTerminals(
            'ProtDecl ProtMethods FullyTypedArgs FullyTypedTail TypeList')

        Body_Arrow=G.NonTerminal("BodyArrow")
        number_, string_, bool_, const_, self_, id_, type_id_ = G.Terminals('number string bool const self id type_id')
        let_, in_, if_, elif_, else_, while_, for_, as_, is_, new_ = G.Terminals('let in if elif else while for as is new')
        function_, type_, inherits_, protocol_, extends_ = G.Terminals('function type inherits protocol extends')
        plus_, minus_, star_, div_, mod_, pow_, power_ = G.Terminals('+ - * / % ^ **') #TODO: Unificar bajo Regex ^ **
        eq_, colon_eq_, eq_qu_, not_eq_, less_, greater_, leq_, geq_ = G.Terminals('= := == != < > <= >=')
        and_, or_, not_, or_or_ = G.Terminals('& | ! ||')
        dot_, comma_, colon_, semi_colon_, at_, at_at_, arrow_ = G.Terminals('. , : ; @ @@ =>')
        o_par_, c_par_, o_brack_, c_brack_, o_brace_, c_brace_ = G.Terminals('( ) [ ] { }')

        space=G.Terminal("space")

        # self_=G.Terminal("self")

        comments=G.Terminal("comments")


        Program %= Declaration_List + Statment, lambda h, s: ProgramNode(s[1], s[2])
        Program %= Declaration_List, lambda h, s: ProgramNode(s[1], [])

        Declaration_List %= Declaration + Declaration_List, lambda h, s: [s[1]] + s[2]
        Declaration_List %= G.Epsilon, lambda h, s: []

        Declaration %= Func_Declaration, lambda h, s: s[1]
        Declaration %= Type_Declaration, lambda h, s: s[1]
        Declaration %= Protocol_Declaration, lambda h, s: s[1]
        #Declaration %= G.Epsilon agregar nueva

        Statment %= Simple_Expresion + semi_colon_, lambda h, s: s[1]
        Statment %= ExprBlock, lambda h, s: s[1]
        Statment %= ExprBlock + semi_colon_, lambda h, s: s[1]
        #Statment %= G.Epsilon TODO: Agregar para que que se puedan hacer solo declaraciones

        Expresion %= Simple_Expresion, lambda h, s: s[1]
        Expresion %= ExprBlock, lambda h, s: s[1]

        Simple_Expresion %= let_ + Assigment_List + in_ + Simple_Expresion, lambda h, s: LetNode(s[2], s[4])
        Simple_Expresion %= if_ + o_par_ + Expresion + c_par_ + Expresion + Elif_Branch + else_ + Simple_Expresion, lambda h, s: IfNodeExpression(s[3], s[5],
                                                                                                           ElifNodeExpressionList(s[6]), s[8])
        Simple_Expresion %= while_ + o_par_ + Expresion + c_par_ + Simple_Expresion, lambda h, s: WhileExpressionNode(s[3], s[5])
        Simple_Expresion %= for_ + o_par_ + id_ + in_ + Expresion + c_par_ + Simple_Expresion, lambda h, s: ForExpressionNode(s[3], s[5], s[7])
        Simple_Expresion %= id_ + colon_eq_ + Simple_Expresion, lambda h, s: DestructionAssignmentBasicExpression(s[1], s[3])
        Simple_Expresion %= Attr_Call + colon_eq_ + Simple_Expresion, lambda h, s: DestructionAssignmentWithAttributeCallExpression(s[1], s[3])
        Simple_Expresion %= Arithmethic_expression, lambda h, s: s[1]

        ExprBlock %= o_brace_ + StatList + c_brace_, lambda h, s: ExpressionBlockNode(s[2])
        ExprBlock %= let_ + Assigment_List + in_ + ExprBlock, lambda h, s: LetNode(s[2], s[4])
        ExprBlock %= if_ + o_par_ + Expresion + c_par_ + Expresion + Elif_Branch + else_ + ExprBlock, lambda h, s: IfNodeExpression(s[3], s[5],
                                                                                                         ElifNodeExpressionList(s[6]), s[8])
        ExprBlock %= while_ + o_par_ + Expresion + c_par_ + ExprBlock, lambda h, s: WhileExpressionNode(s[3], s[5])
        ExprBlock %= for_ + o_par_ + id_ + in_ + Expresion + c_par_ + ExprBlock, lambda h, s: ForExpressionNode(s[3], s[5], s[7])
        ExprBlock %= id_ + colon_eq_ + ExprBlock, lambda h, s: DestructionAssignmentBasicExpression(s[1], s[3])
        ExprBlock %= Attr_Call + colon_eq_ + ExprBlock, lambda h, s: DestructionAssignmentWithAttributeCallExpression(s[1], s[3])

        StatList %= Statment, lambda h, s: [s[1]]
        StatList %= Statment + StatList, lambda h, s: [s[1]] + s[2]

        Expression_List %= Expresion + Expression_Trail, lambda h, s: [s[1]] + s[2]
        Expression_List %= G.Epsilon, lambda h, s: []

        Expression_Trail %= comma_ + Expresion + Expression_Trail, lambda h, s: [s[2]] + s[3]
        Expression_Trail %= G.Epsilon, lambda h, s: []

        Assigment_List %= Var_Declaration + eq_ + Expresion, lambda h, s: [AssignNode(s[1], s[3])]
        Assigment_List %= Var_Declaration + eq_ + Expresion + comma_ + Assigment_List, lambda h, s: [AssignNode(s[1], s[3])] + s[5]

        Var_Declaration %= id_, lambda h, s: VarDefNode(s[1])
        Var_Declaration %= id_ + colon_ + type_id_, lambda h, s: VarDefNode(s[1], s[3])

        Elif_Branch %= elif_ + o_par_ + Expresion + c_par_ + Expresion + Elif_Branch, lambda h, s: [ElifNodeAtomExpression(s[3], s[5])] + s[6]
        Elif_Branch %= G.Epsilon, lambda h, s: []

        Arithmethic_expression %= Disjoin, lambda h, s: s[1]
        Arithmethic_expression %= Arithmethic_expression + at_ + Disjoin, lambda h, s: ConcatNode(s[1], s[3])
        Arithmethic_expression %= Arithmethic_expression + at_at_ + Disjoin, lambda h, s: ConcatWithSpaceNode(s[1], s[3])

        Disjoin %= Conj, lambda h, s: s[1]
        Disjoin %= Disjoin + or_ + Conj, lambda h, s: OrNode(s[1], s[3])

        Conj %= Negation, lambda h, s: s[1]
        Conj %= Conj + and_ + Negation, lambda h, s: AndNode(s[1], s[3])

        Negation %= Dyn_Test, lambda h, s: s[1]
        Negation %= not_ + Dyn_Test, lambda h, s: NotNode(s[2])

        Dyn_Test %= Comp, lambda h, s: s[1]
        Dyn_Test %= Comp + is_ + type_id_, lambda h, s: DynTestNode(s[1], s[3])

        Comp %= Number_Expression, lambda h, s: s[1]
        Comp %= Number_Expression + eq_qu_ + Number_Expression, lambda h, s: EqualNode(s[1], s[3])
        Comp %= Number_Expression + not_eq_ + Number_Expression, lambda h, s: NotEqualNode(s[1], s[3])
        Comp %= Number_Expression + less_ + Number_Expression, lambda h, s: LessNode(s[1], s[3])
        Comp %= Number_Expression + greater_ + Number_Expression, lambda h, s: GreaterNode(s[1], s[3])
        Comp %= Number_Expression + leq_ + Number_Expression, lambda h, s: LeqNode(s[1], s[3])
        Comp %= Number_Expression + geq_ + Number_Expression, lambda h, s: GeqNode(s[1], s[3])

        Number_Expression %= Term, lambda h, s: s[1]
        Number_Expression %= Number_Expression + plus_ + Term, lambda h, s: PlusNode(s[1], s[3])
        Number_Expression %= Number_Expression + minus_ + Term, lambda h, s: MinusNode(s[1], s[3])

        Term %= Factor, lambda h, s: s[1]
        Term %= Term + star_ + Factor, lambda h, s: StarNode(s[1], s[3])
        Term %= Term + div_ + Factor, lambda h, s: DivNode(s[1], s[3])
        Term %= Term + mod_ + Factor, lambda h, s: ModNode(s[1], s[3])

        Factor %= Sign, lambda h, s: s[1]
        Factor %= Sign + pow_ + Factor, lambda h, s: PowNode(s[1], s[3])
        Factor %= Sign + power_ + Factor, lambda h, s: PowNode(s[1], s[3])

        Sign %= Atomic, lambda h, s: s[1]
        Sign %= minus_ + Atomic, lambda h, s: NegativeNode(s[2])

        Atomic %= number_, lambda h, s: LiteralNumNode(s[1])
        Atomic %= string_, lambda h, s: LiteralStrNode(s[1])
        Atomic %= bool_, lambda h, s: LiteralBoolNode(s[1])
        Atomic %= const_, lambda h, s: ConstantNode(s[1])
        Atomic %= id_, lambda h, s: VarNode(s[1])
        Atomic %= o_brack_ + Expression_List + c_brack_, lambda h, s: VectorNode(s[2])
        Atomic %= o_brack_ + Expresion + or_or_ + id_ + in_ + Expresion + c_brack_, lambda h, s: ImplicitVector(s[2], s[4], s[6])
        Atomic %= new_ + type_id_ + o_par_ + Expression_List + c_par_, lambda h, s: InstantiateNode(s[2], s[4])
        Atomic %= Atomic + as_ + type_id_, lambda h, s: DowncastNode(s[1], s[3])
        Atomic %= Atomic + o_brack_ + Expresion + c_brack_, lambda h, s: IndexingNode(s[1], s[3])
        # Atomic %= o_par_ + Expresion + c_par_, lambda h, s: s[2]  # Mira aqui el problema                        -------------- Ahhhhhh ----------

        Atomic %= Attr_Call, lambda h, s: s[1]
        Atomic %= Closed_Expression, lambda h, s: s[1]
        Atomic %= Function_Call, lambda h, s: s[1]
        Atomic %= Method_Call, lambda h, s: MethodCallListNode(s[1])
        
        Attr_Call %= self_ + dot_ + id_, lambda h, s: AttrCallNode(s[3])  # self.x
        Function_Call %= id_ + o_par_ + Expression_List + c_par_, lambda h, s: FunctionCallNode(s[1], s[3])   #  sin(180)
        Closed_Expression %= o_par_ + Expresion + c_par_, lambda h, s: s[2]

        # Atomic %= id_ + dot_ + id_ + o_par_ + Expression_List + c_par_, lambda h, s: MethodCallNode(s[1], s[3], s[5])  # TODO: This was the original
        #Llamar con el self
        Method_Call %= self_ + dot_ + id_ + o_par_ + Expression_List + c_par_ + Method_Call_List, lambda h, s: [MethodCallWithIdentifierNode(s[1], s[3], s[5])] + s[7]   # self.something()
        #llamar una funcion de otro tipo en un tipo
        Method_Call %= Attr_Call + dot_ + id_ + o_par_ + Expression_List + c_par_ + Method_Call_List, lambda h, s: [MethodCallWithExpressionNode(s[1], s[3], s[5])] + s[7]  # self.x.something()
        #llamar un metodo normal
        Method_Call %= id_ + dot_ + id_ + o_par_ + Expression_List + c_par_ + Method_Call_List, lambda h, s: [MethodCallWithIdentifierNode(s[1], s[3], s[5])] + s[7]    # x.something()
        #llamada desde una fucnion normal
        Method_Call %= Function_Call + dot_ + id_ + o_par_ + Expression_List + c_par_ + Method_Call_List, lambda h, s: [MethodCallWithExpressionNode(s[1], s[3], s[5])] + s[7]   # get_default_triangle().get_point(1).get_norm()
        #llamada con expresion node
        Method_Call %= Closed_Expression + dot_ + id_ + o_par_ + Expression_List + c_par_ + Method_Call_List, lambda h, s: [MethodCallWithExpressionNode(s[1], s[3], s[5])] + s[7]   # (expression).get_something()
        #TODO: revisar para quitar lo de abajo
        Method_Call_List %= dot_ + id_ + o_par_ + Expression_List + c_par_ + Method_Call_List, lambda h, s: [MethodCallWithIdentifierNode('result', s[2], s[4])] + s[6]
        Method_Call_List %= G.Epsilon, lambda h, s: []


        Func_Declaration %= function_ + id_ + o_par_ + Argument_List + c_par_ + Body, lambda h, s: FunctionDeclarationNode(s[2], s[4], s[6])
       #TODO:new Func_Declaration %= id_ + o_par_ + Argument_List + c_par_ +arrow_+, lambda h, s: FunctionDeclarationNode(s[2], s[4], s[6])
        Func_Declaration %= function_ + id_ + o_par_ + Argument_List + c_par_ + colon_ + type_id_ + Body, lambda h, s: FunctionDeclarationNode(s[2],
                                                                                                                                               s[4],
                                                                                                                                s[8],
                                                                                                                                               s[7])

        #TODO:NEW
        #Body_Arrow %= Statment, lambda h, s: s[1]
        #Body_Arrow %=o_brace_ + StatList + c_brace_, lambda h, s: s[2]


        #####
        Body %= arrow_ + Statment, lambda h, s: s[2]
        Body %= o_brace_ + StatList + c_brace_, lambda h, s: s[2]

        Argument_List %= Var_Declaration + Arg_Tail, lambda h, s: [s[1]] + s[2]
        Argument_List %= G.Epsilon, lambda h, s: []

        Arg_Tail %= comma_ + Var_Declaration + Arg_Tail, lambda h, s: [s[2]] + s[3]
        Arg_Tail %= G.Epsilon, lambda h, s: []

        Type_Declaration %= type_ + type_id_ + o_brace_ + Feature_List + c_brace_, lambda h, s: TypeDeclarationNode(s[2], s[4])
        Type_Declaration %= type_ + type_id_ + o_par_ + Argument_List + c_par_ + o_brace_ + Feature_List + c_brace_, lambda h, s: TypeDeclarationNode(
            s[2], s[7], s[4])
        Type_Declaration %= type_ + type_id_ + inherits_ + type_id_ + o_brace_ + Feature_List + c_brace_, lambda h, s: TypeDeclarationNode(s[2],
                                                                                                                                           s[6],
                                                                                                                                           [],
                                                                                                                                           s[4])
        Type_Declaration %= type_ + type_id_ + o_par_ + Argument_List + c_par_ + inherits_ + type_id_ + o_par_ + Expression_List + c_par_ + o_brace_ + Feature_List + c_brace_, lambda \
            h, s: TypeDeclarationNode(s[2], s[12], s[4], s[7], s[9])

        Feature_List %= Var_Declaration + eq_ + Statment + Feature_List, lambda h, s: [AssignNode(s[1], s[3])] + s[4]
        Feature_List %= id_ + o_par_ + Argument_List + c_par_ + Body + Feature_List, lambda h, s: [MethodNode(s[1], s[3], s[5])] + s[
            6]
        Feature_List %= id_ + o_par_ + Argument_List + c_par_ + colon_ + type_id_ + Body + Feature_List, lambda h, s: [MethodNode(s[1],
                                                                                                                   s[3],
                                                                                                                   s[7],
                                                                                                                   s[
                                                                                                                       6])] +  s[8]


        Feature_List %= G.Epsilon, lambda h, s: []

        Protocol_Declaration %= protocol_ + type_id_ + o_brace_ + Protocol_Methods + c_brace_, lambda h, s: ProtocolDeclarationNode(s[2], s[4])
        Protocol_Declaration %= protocol_ + type_id_ + extends_ + Type_List + o_brace_ + Protocol_Methods + c_brace_, lambda h, s: ProtocolDeclarationNode(
            s[2], s[6], s[4])

        Protocol_Methods %= id_ + o_par_ + Full_Type_Arguments + c_par_ + colon_ + type_id_ + semi_colon_ + Protocol_Methods, lambda h, s: [
                                                                                                                  ProtocolMethodNode(
                                                                                                                      s[
                                                                                                                          1],
                                                                                                                      s[
                                                                                                                          3],

                                                                                                                      s[
                                                                                                                          6])] + \
                                                                                                              s[8]

        Protocol_Methods %= G.Epsilon, lambda h, s: []

        Full_Type_Arguments %= id_ + colon_ + type_id_ + Fully_Typed_Tail, lambda h, s: [VarDefNode(s[1], s[3])] + s[4]
        Full_Type_Arguments %= G.Epsilon, lambda h, s: []

        Fully_Typed_Tail %= comma_ + id_ + colon_ + type_id_ + Fully_Typed_Tail, lambda h, s: [VarDefNode(s[2], s[4])] + s[5]
        Fully_Typed_Tail %= G.Epsilon, lambda h, s: []

        Type_List %= type_id_, lambda h, s: [s[1]]
        Type_List %= type_id_ + comma_ + Type_List, lambda h, s: [s[1]] + s[3]
