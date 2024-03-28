from cmp.pycompiler import *  # Gramar Terminal NonTerminal Token
from cmp.cil import *
from Hulk.AST_Semantic.Ast import *





class Gramarlr1:
    def __init__(self) -> None:
        G = Grammar()
        self.Grammar = G
        self.EOF=self.Grammar.EOF

        # # non-terminals
        program = G.NonTerminal("<program>", startSymbol=True)
        exp, exp_block, exp_list = G.NonTerminals("<exp> <exp-block> <exp-list>")
        def_func = G.NonTerminal("<def-func>")
        end_extended = G.NonTerminal("<end-extended>")
        param_list, param = G.NonTerminals("<param-list> <param>")
        arg_declaration = G.NonTerminal("<arg-declaration>")
        let_exp, assign_var, assign_list = G.NonTerminals("<let-exp> <assign-var> <assign-list>")
        mutate_var = G.NonTerminal("<mutate-var>")
        conditional, condition = G.NonTerminals("<conditional> <condition>")
        elif_block = G.NonTerminal("<elif-block>")
        while_block = G.NonTerminal("<while-block>")
        for_exp = G.NonTerminal("<for-exp>")
        type_dec = G.NonTerminal("<type-dec>")
        term, factor, atom, k, mod_ = G.NonTerminals("<term> <factor> <atom> <k> <mod>")
        statement = G.NonTerminal("<statement>")
        def_protocol = G.NonTerminal("<def-protocol>")
        method_declarations = G.NonTerminal("<method-declarations>")
        def_method = G.NonTerminal("<def-method>")
        instance = G.NonTerminal("<instance>")
        # exp_or_block = G.NonTerminal("<exp-or-block>")
        list_ = G.NonTerminal("<list>")
        type_body, type_args = G.NonTerminals("<type-body> <type-args>")
        attribute = G.NonTerminal("<attribute>")
        vector, iterable = G.NonTerminals("<vector> <iterable>")
        func_call = G.NonTerminal("<func-call>")
        print_exp = G.NonTerminal("<print-exp>")
        string_exp = G.NonTerminal("<string-exp>")
        concatenable = G.NonTerminal("<concatenable>")
        functions_in_type = G.NonTerminal("<functions-in-type>")
        indexation = G.NonTerminal("<indexation>")
        boolean_exp = G.NonTerminal("<boolean>")
        conforms = G.NonTerminal("<conforms>")
        possible_types = G.NonTerminal("<poss-types>")
        concatenable_cond = G.NonTerminal("<bool-ext>")
        statement_list = G.NonTerminal("<stat-list>")
        id_list = G.NonTerminal("<id-list")
        call_name = G.NonTerminal("<call-name>")
        single_func_call = G.NonTerminal("<sing-func-call>")
        multiple_func_call = G.NonTerminal("<mult-func>")
        #
        #
        # region TERMINALS
        curly_o , curly_c = G.Terminals("{ }")
        square_o, square_c = G.Terminals("[ ]")
        semi_colon , colon = G.Terminals("; :")
        opar, cpar = G.Terminals("( )")
        rarrow, given = G.Terminals("=> ||")
        comma, dot = G.Terminals(", .")
        let, inx = G.Terminals("let in")
        equal, mut = G.Terminals("= :=")
        ifx, elsex, elifx, whilex, forx, function = G.Terminals("if else elif while for function")
        leq, less, equals, geq, greater, neq = G.Terminals("<= < == >= > !=")
        sqrt, cos, sin, expon, log, rand = G.Terminals("sqrt cos sin expon log rand")
        plus, minus, star, div, mod, pow, num, notx, andx, orx = G.Terminals("+ - * / % ^ num ! & |")
        typex, new, inherits, isx, asx = G.Terminals("type new inherits is as")
        protocol, extends = G.Terminals("protocol extends")
        true, false = G.Terminals("true false")
        concat, concat_space = G.Terminals("@ @@")
        strx, idx, boolx, string, intx, base = G.Terminals("str id bool string int base")

        rangex = G.Terminal("range")
        printx = G.Terminal("print")
        PI, E = G.Terminals("PI E")
        #
        #
        # #productions
        #
        # # ------esto no me queda muy claro

        program %= statement_list + exp + semi_colon, lambda h, s: ProgramNode(s[1], [s[2]])
        program %= statement_list + exp, lambda h,s: ProgramNode(s[1], [s[2]])
        program %= statement_list + exp_block, lambda h, s: ProgramNode(s[1], s[2])
        program %= statement_list + exp_block + semi_colon, lambda h, s: ProgramNode(s[1], s[2])

        statement_list %= def_protocol + statement_list, lambda h, s: [s[1]] + s[2]
        statement_list %= type_dec + statement_list, lambda h, s: [s[1]] + s[2]
        statement_list %= def_func + statement_list, lambda h, s: [s[1]] + s[2]
        statement_list %= G.Epsilon, lambda h,s: []
        # statement %= exp + semi_colon, lambda h, s: s[1]
        # # statement %= exp, lambda h, s: s[1]
        # statement %= exp_block, lambda h, s: s[1]
        # statement %= exp_block + semi_colon, lambda h, s: s[1]

        exp %= while_block, lambda h, s: s[1]
        exp %= for_exp, lambda h, s: s[1]
        exp %= print_exp, lambda h, s: s[1]
        exp %= instance, lambda h, s: s[1]
        exp %= mutate_var, lambda h, s: s[1]
        exp %= string_exp, lambda h, s: s[1]
        exp %= iterable, lambda h, s: s[1]
        string_exp %= conforms, lambda h, s: s[1]

        string_exp %= let_exp, lambda h, s: s[1]
        string_exp %= conditional, lambda h, s: s[1]

        string_exp %= indexation + concatenable, lambda h, s: StringExpression(s[1], s[2])
        string_exp %= indexation, lambda h,s: s[1]

        string_exp %= term + concatenable, lambda h, s: StringExpression(s[1],s[2])
        string_exp %= term, lambda h,s: s[1]

        string_exp %= strx + concatenable, lambda h, s: StringExpression(ConstantStringNode(s[1]), s[2])
        string_exp %= strx, lambda h,s: ConstantStringNode(s[1].lex)


        concatenable %= concat + string_exp, lambda h, s: StringExpression(ConstantStringNode(""), s[2])
        concatenable %= concat_space + string_exp, lambda h, s: StringExpression(ConstantStringNode(" "),s[2])

        #---------- Protocol Declaration Stuff ----------------
        def_protocol %= protocol + idx + curly_o + method_declarations + curly_c, lambda h, s: ProtocolDeclarationNode(s[2], s[4], None)
        def_protocol %= protocol + idx + extends + id_list + curly_o + method_declarations + curly_c, lambda h, s: ProtocolDeclarationNode(s[2], s[6], s[4])

        id_list %= idx, lambda h,s: [s[1]]
        id_list %= idx + comma + id_list, lambda h,s: [s[1]] + s[3]

        def_method %= idx + opar + param_list + cpar + colon + possible_types, lambda h, s: MethodDeclaration(s[1], s[3], s[6])

        # method_declarations %= G.Epsilon, lambda h,s: []
        method_declarations %= def_method + semi_colon, lambda h, s: [s[1]]
        method_declarations %= def_method + semi_colon + method_declarations, lambda h, s: [s[1]] + s[3]

        #-----------Type Declaration Stuff ---------------------
        type_dec %= typex + idx + type_args + curly_o + type_body + curly_c, lambda h, s: TypeDeclarationNode(s[2], s[5], None, s[3])
        type_dec %= typex + idx + inherits + idx + curly_o + type_body + curly_c, lambda h, s: TypeDeclarationNode(s[2], s[6], s[4], None)
        #empty body
        type_dec %= typex + idx + inherits + idx + curly_o + curly_c, lambda h, s: TypeDeclarationNode(s[2], [], s[4], None)
        type_dec %= typex + idx + type_args + curly_o + curly_c, lambda h, s: TypeDeclarationNode(s[2], [], None, s[3])

        type_args %= opar + param_list + cpar, lambda h, s: s[2]
        type_args %= G.Epsilon, lambda h, s: []

        type_body %= functions_in_type, lambda h, s: [s[1]]
        type_body %= functions_in_type + type_body, lambda h, s: [s[1]] + s[3]
        type_body %= attribute + semi_colon, lambda h, s: [s[1]]
        type_body %= attribute + semi_colon + type_body, lambda h, s: [s[1]] + s[3]

        functions_in_type %= idx + opar + param_list + cpar + rarrow + exp + semi_colon, lambda h, s: FuncDeclarationNode(s[1], s[3], s[6])
        functions_in_type %= idx + opar + param_list + cpar + exp_block, lambda h, s: FuncDeclarationNode(s[1], s[3], s[5])

        attribute %= idx + equal + exp, lambda h, s: AttrDeclarationNode(s[1], s[3], None)
        attribute %= idx + colon + possible_types, lambda h, s: AttrDeclarationNode(s[1], None, s[3])

        instance %= new + idx + opar + param_list + cpar, lambda h, s: InstantiateNode(s[2], s[4])

        exp_block %= curly_o + exp_list + curly_c, lambda h, s: s[2]

        exp_list %= exp + semi_colon + exp_list, lambda h, s: [s[1]] + s[3]
        exp_list %= exp + semi_colon, lambda h, s: [s[1]]

        def_func %= function + idx + opar + param_list + cpar + rarrow + exp + semi_colon, lambda h, s: FuncDeclarationNode(s[2], s[4], s[7])
        def_func %= function + idx + opar + param_list + cpar + exp_block, lambda h, s: FuncDeclarationNode(s[2], s[4], s[6])

        func_call %= idx + dot + idx, lambda h,s: AttrCallNode(s[1], s[3])
        func_call %= idx + dot + multiple_func_call, lambda h,s : FuncCallNode(s[1],[s[3]])
        func_call %= multiple_func_call, lambda h,s: s[1]

        multiple_func_call %= single_func_call , lambda h,s: s[1]
        multiple_func_call %= single_func_call + dot + multiple_func_call, lambda h,s: FuncCallNode(s[1], [s[3]])

        single_func_call %= idx + opar + param_list + cpar, lambda h,s: FuncCallNode(s[1], s[3])

        param_list %= param, lambda h, s: [s[1]]
        param_list %= param + comma + param_list, lambda h, s: [s[1]] + s[3]

        arg_declaration %= idx + colon + possible_types, lambda h, s: (s[1],s[3])
        arg_declaration %= term, lambda h,s: (s[1],None)
        arg_declaration %= G.Epsilon, lambda h, s: (VoidNode(None),None)

        param %= arg_declaration, lambda h, s: s[1]

        let_exp %= let + assign_list + inx + exp, lambda h, s: LetNode(s[2], [s[4]])
        let_exp %= let + assign_list + inx + exp_block, lambda h, s: LetNode(s[2], s[4])

        assign_list %= assign_var, lambda h, s: [s[1]]
        assign_list %= assign_var + comma + assign_list, lambda h, s: [s[1]] + s[3]

        assign_var %= idx + equal + exp, lambda h, s: AssignNode(s[1], s[3])

        mutate_var %= idx + mut + exp, lambda h, s: DestructiveAssignment(s[1], s[3])

        conditional %= ifx + opar + boolean_exp + cpar + exp + elif_block, lambda h, s: ConditionalNode(s[3], [s[5]], s[6])
        conditional %= ifx + opar + boolean_exp + cpar + exp_block + elif_block, lambda h, s: ConditionalNode(s[3], s[5], s[6])

        elif_block %= elsex + exp, lambda h, s: ElseBlockNode([s[2]])
        elif_block %= elsex + exp_block, lambda h, s: ElseBlockNode(s[2])
        elif_block %= elifx + opar + boolean_exp + cpar + exp + elif_block, lambda h, s: ConditionalNode(s[3], [s[5]], s[6])
        elif_block %= elifx + opar + boolean_exp + cpar + exp_block + elif_block, lambda h, s: ConditionalNode(s[3], s[5], s[6])

        while_block %= whilex + opar + boolean_exp + cpar + exp + elsex + exp , lambda h, s: LoopNode(s[3], [s[5]], [s[7]])
        while_block %= whilex + opar + boolean_exp + cpar + exp + elsex + exp_block, lambda h, s: LoopNode(s[3], [s[5]], s[7])
        while_block %= whilex + opar + boolean_exp + cpar + exp_block + elsex + exp , lambda h, s: LoopNode(s[3], s[5], [s[7]])
        while_block %= whilex + opar + boolean_exp + cpar + exp_block + elsex + exp_block, lambda h, s: LoopNode(s[3], s[5], s[7])

        for_exp %= forx + opar + idx + inx + exp + cpar + exp + elsex + exp, lambda h, s: ForNode(s[5],[s[7]],s[3], s[9])
        for_exp %= forx + opar + idx + inx + exp + cpar + exp + elsex + exp_block, lambda h, s: ForNode(s[5],[s[7]],s[3], s[9])
        for_exp %= forx + opar + idx + inx + exp + cpar + exp_block + elsex + exp, lambda h, s: ForNode(s[5],s[7],s[3],s[9])
        for_exp %= forx + opar + idx + inx + exp + cpar + exp_block + elsex + exp_block, lambda h, s: ForNode(s[5],s[7],s[3],s[9])

        iterable %= vector, lambda h, s: s[1]
        iterable %= rangex + opar + exp + comma + exp + cpar, lambda h, s: RangeNode(s[3], s[5])

        vector %= square_o + list_ + square_c, lambda h, s: s[2]
        vector %= square_o + exp + given + idx + inx + iterable + square_c, lambda h, s: List_Comprehension(s[4], [s[2]],s[6])

        list_ %= exp, lambda h, s: [s[1]]
        list_ %= exp + comma + list_, lambda h, s: [s[1]] + s[3]

        indexation %= idx + square_o + exp + square_c, lambda h, s: IndexationNode(s[1], s[3])
        indexation %= iterable + square_o + exp + square_c, lambda h, s: IndexationNode(s[1], s[3])
        indexation %= func_call + square_o + exp + square_c, lambda h,s: IndexationNode(s[1], s[3])

        term %= factor, lambda h, s: s[1]
        term %= term + plus + factor, lambda h, s: PlusNode(s[1], s[3])
        term %= term + minus + factor, lambda h, s: MinusNode(s[1], s[3])

        factor %= mod_, lambda h, s: s[1]
        factor %= factor + star + mod_, lambda h, s: StarNode(s[1], s[3])
        factor %= factor + div + mod_, lambda h, s: DivNode(s[1], s[3])

        mod_ %= k, lambda h, s: s[1]
        mod_ %= mod_ + mod + k, lambda h, s: ModNode(s[1], s[3])

        k %= atom, lambda h, s: s[1]
        k %= k + pow + atom, lambda h, s: PowNode(s[1], s[3])

        atom %= idx, lambda h, s: VariableNode(s[1])
        atom %= num, lambda h, s: ConstantNumNode(s[1])
        atom %= minus + num, lambda h, s: NegNode(ConstantNumNode(s[2]))
        atom %= opar + exp + cpar, lambda h, s: s[2]
        atom %= sqrt + opar + exp + cpar, lambda h, s: SqrtNode(s[3])
        atom %= cos + opar + exp + cpar, lambda h, s: CosNode(s[3])
        atom %= sin + opar + exp + cpar, lambda h, s: SinNode(s[3])
        atom %= expon + opar + exp + cpar, lambda h, s: ExponEulerNode(s[3])
        atom %= log + opar + exp + comma + exp + cpar, lambda h, s: LogNode(s[3], s[5])
        atom %= rand + opar + cpar, lambda h, s: RandNode(s[2])
        atom %= PI, lambda h, s: ConstantNumNode(s[1])
        atom %= E, lambda h, s: ConstantNumNode(s[1])
        atom %= func_call, lambda h, s: s[1]

        #boolean expressions as described in hulk
        #TODO: (condition)
        #TODO: check all AST nodes
        condition %= exp + leq + exp, lambda h, s: LeqNode(s[1], s[3])
        condition %= exp + less + exp, lambda h, s: LessNode(s[1], s[3])
        condition %= exp + equals + exp, lambda h, s: EqualNode(s[1], s[3])
        condition %= exp + geq + exp, lambda h, s: LessNode(s[3], s[1])
        condition %= exp + greater + exp, lambda h, s: LeqNode(s[3], s[1])
        condition %= exp + neq + exp, lambda h, s: NotNode(EqualNode(s[1], s[3]))

        condition %= true, lambda h, s: ConstantBoolNode(s[1])
        condition %= false, lambda h, s: ConstantBoolNode(s[1])
        condition %= opar + exp + cpar, lambda h, s: s[2]
        condition %= notx + exp, lambda h, s: NotNode(s[2])
        condition %= exp + isx + possible_types, lambda h, s: IsNode(s[1], s[3])
        condition %= func_call, lambda h,s: s[1]
        condition %= idx, lambda h,s: s[1]

        concatenable_cond %= condition + andx + concatenable_cond, lambda h,s: AndNode(s[1], s[3])
        concatenable_cond %= condition + orx + concatenable_cond, lambda h,s: OrNode(s[1], s[3])
        concatenable_cond %= condition, lambda h,s: s[1]

        boolean_exp %= concatenable_cond, lambda h,s: s[1]

        print_exp %= printx + opar + exp + cpar, lambda h, s: PrintNode(s[3])

        conforms %= term + asx + possible_types, lambda h,s: ConformsNode(s[1], s[3])

        possible_types %= idx, lambda h,s: s[1]
        possible_types %= string, lambda h,s : s[1]
        possible_types %= boolx, lambda h,s: s[1]
        possible_types %= intx, lambda h,s: s[1]