from pycompiler import * # Gramar Terminal NonTerminal Token
from cil import *

class Gramarlr1:
    def __init__(self) ->None:
        
        G = Grammar()

        # NonTerminal
        Program, Expression, Statement = G.NonTerminal('Program Expression Statement')

        Parameters, FunctionStyle, TypeDef, ProtocolDeclare = G.NonTerminal('Parameters FunctionStyle TyoeDef ProtocolDeclare')
        
        SimpleExpression, ExpressionBlock = G.NonTerminal('SimpleExpression ExpressionBlock')
        
        ParameterList = G.NonTerminal('ParameterList')
        
        Variable = G.NonTerminal('Variable')
        
        ClassBlock, ArgumentList = G.NonTerminal('ClassBlock ArgumentList')
        
        ClassDeclaration, ClassBody = G.NonTerminal('ClassDeclaration ClassBody')
        
        ProtocolBody = G.NonTerminal('ProtocolBody')
        
        TypeParameters = G.NonTerminal('TypeParameters')
        
        TypeParametersList = G.NonTerminal('TypeParametersList')
        
        Declaration = G.NonTerminal('Declaration')

        IfBlock, ElseBlock, Disjuntion, Arguments = G.NonTerminal('IfBlock ElseBlock Disjuntion Arguments') 
        
        Conjunction = G.NonTerminal('Conjunction')

        Literal =G.NonTerminal('Literal')

        Proposition = G.NonTerminal('Proposition')
        
        Boolean = G.NonTerminal('Boolean')

        Concatenation =G.NonTerminal('Concatenation')
        # Terminal

        function, name, type = G.Terminal('function <name> type')

        semi, comma, opar, cpar, arrow, okey, ckey, colon = G.Terminals('; , ( ) => { } :')
        
        inherints = G.Terminal('inherints')

        equal = G.Terminal('=')

        protocol, extends = G.Terminal('protocol extends')
        
        let, inn, iff, whilee, forr, neww, destruct = G.Terminal('let in  if while for new :=')
        
        elsee, eliff = G.Terminal('else elif')

        orr, andd, nott, iss = G.Terminal('| & ! is')

        eq, neq, lte, gte, lt, gt = G.Terminals('== != <= >= < >')
        #Production
        Program %= Expression, lambda h,s: ProgramNode(s[1])
        Program %= Statement + Program, lambda h,s: s[1], lambda h,s: lambda h,s: s[2]

        Statement %= function +name +Parameters+ FunctionStyle, lambda h,s: s[3], lambda h,s: s[4]
        Statement %= type + name+ TypeDef,lambda h,s : s[3]
        Statement %= ProtocolDeclare, lambda h,s: s[1]

        FunctionStyle %= arrow+ SimpleExpression+ semi, lambda h,s: s[2]
        FunctionStyle %= colon+ name + arrow + SimpleExpression + semi, lambda h,s: s[4]
        FunctionStyle %= okey+ ExpressionBlock+ckey, lambda h,s: s[2]
        FunctionStyle %= colon+ name + okey + ExpressionBlock + ckey, lambda h,s: s[4]

        ParameterList %= opar+cpar
        ParameterList %= opar+ParameterList+cpar

        ParameterList %= Variable,lambda h,s: s[1]
        ParameterList %= Variable+comma+ ParameterList, lambda h,s: s[1], lambda h,s: s[2]

        Variable %= name
        Variable %= name+colon+name

        TypeDef %= ClassBlock, lambda h,s: s[1]
        TypeDef %= inherints+ name+ ClassBlock, lambda h,s: s[3]        
        TypeDef %= opar+ ParameterList+ cpar + ClassBlock, lambda h,s: s[2], lambda h,s: s[4]
        TypeDef %= opar+ParameterList+cpar +inherints+name + ClassBlock, lambda h,s: s[2], lambda h,s: s[6]
        TypeDef %= opar+ParameterList+cpar +inherints+ name+ opar+ ArgumentList+cpar+ClassBlock, lambda h,s: s[2], lambda h,s: s[7], lambda h,s: s[9]
        TypeDef %=inherints+ name+ opar+ ArgumentList+cpar+ClassBlock, lambda h,s: s[4], lambda h,s: s[6]

        ClassBlock  %=()
        ClassBlock %= okey+ ClassBlock+ckey, lambda h,s: s[2]

        ClassBody %= ClassDeclaration,lambda h,s: s[1]
        ClassBody %= ClassDeclaration + ClassBody,lambda h,s: s[1],lambda h,s: s[2]

        ClassDeclaration %= Variable + equal + SimpleExpression+ semi,lambda h,s: s[1], lambda h,s:s[3]
        ClassDeclaration %= FunctionStyle, lambda h,s: s[1]

        ProtocolDeclare %= protocol + name + okey +ProtocolBody +ckey,lambda h,s: s[4]
        ProtocolDeclare %= protocol + name+ extends + name +okey +ProtocolBody +ckey,lambda h,s: s[6]

        ProtocolBody %= name + TypeParameters+ colon +name + semi,lambda h,s: s[2]
        ProtocolBody %= name + TypeParameters+ colon +name + semi+ProtocolBody,lambda h,s: s[2],lambda h,s: s[6]

        TypeParameters %= opar+cpar
        TypeParameters %= opar+TypeParametersList+cpar,lambda h,s: s[2]

        TypeParametersList %= name + colon+ name
        TypeParametersList %= name + colon+ name+ comma+TypeParametersList,lambda h,s: s[5]

        Expression %= SimpleExpression+ semi,lambda h,s: s[1]
        Expression %= okey +ExpressionBlock+ckey,lambda h,s: s[2]

        ExpressionBlock %= Expression
        ExpressionBlock %= ExpressionBlock+ Expression

        SimpleExpression %= let + Declaration+ inn +Expression, lambda h,s: s[2], lambda h,s:s[4]
        SimpleExpression %= name +destruct+ SimpleExpression, lambda h,s: s[3]
        SimpleExpression %= iff + IfBlock+ ElseBlock, lambda h,s: s[2], lambda h,s: s[3]
        SimpleExpression %= whilee+ opar+SimpleExpression+cpar+Expression, lambda h,s: s[3],lambda h,s: s[5]
        SimpleExpression %= forr+opar+name + inn+SimpleExpression+cpar+Expression, lambda h,s: s[5],lambda h,s: s[7]
        SimpleExpression %= neww+ name + Arguments, lambda h,s: s[3]
        SimpleExpression %= Disjuntion, lambda h,s: s[1]

        Declaration %= Variable + equal+ SimpleExpression, lambda h,s: s[1],lambda h,s: s[3]
        Declaration %= Variable + equal+ SimpleExpression+comma+Declaration, lambda h,s: s[1],lambda h,s: s[3], lambda h,s: s[5]
        
        IfBlock %= opar+SimpleExpression+cpar+SimpleExpression, lambda h,s: s[2], lambda h,s: s[4]
        IfBlock %= opar+SimpleExpression+cpar+okey+ExpressionBlock+ckey, lambda h,s: s[2], lambda h,s: s[5]

        ElseBlock %= elsee+ Expression, lambda h,s: s[2]
        ElseBlock %= eliff+ IfBlock+ ElseBlock, lambda h,s: s[3]

        Arguments %= opar+cpar
        Arguments %= opar+ArgumentList+cpar,lambda h,s: s[2]

        Disjuntion %= Conjunction, lambda h,s: s[1]
        Disjuntion %= Conjunction+orr+ Disjuntion , lambda h,s: s[1] , lambda h,s: s[3]

        Conjunction %= Literal, lambda h,s: s[1]
        Conjunction %= Literal+ andd+ Conjunction, lambda h,s: s[1],lambda h,s: s[3
                                                                                  ]
        Literal %= Proposition, lambda h,s: s[1]
        Literal %= nott+Literal,lambda h,s: s[2]

        Proposition %= Boolean,lambda h,s: s[1]
        Proposition %= Proposition+ iss+ name,lambda h,s: s[1]

        Boolean %= Concatenation, lambda h,s: s[1]
        Boolean %= Boolean +eq+ Concatenation, lambda h,s: s[1], lambda h,s: s[3]
        Boolean %= Boolean +neq+ Concatenation, lambda h,s: s[1], lambda h,s: s[3]
        Boolean %= Boolean +lte+ Concatenation, lambda h,s: s[1], lambda h,s: s[3]
        Boolean %= Boolean +gte+ Concatenation, lambda h,s: s[1], lambda h,s: s[3]
        Boolean %= Boolean +lt+ Concatenation, lambda h,s: s[1], lambda h,s: s[3]
        Boolean %= Boolean +gt+ Concatenation, lambda h,s: s[1], lambda h,s: s[3]
        
        Concatenation%= 







