from enum import Enum
import uuid
class TagsEnum(Enum):
    Var_ID_Node = 29
    Null = -2
    UNKNOWN = -1
    IndexingNode = 28
    VectorNode = 27
    WhileNode = 26
    ElifNodeAtom = 25
    IfNode = 24
    ForExpressionNode = 23
    DownCastNode = 22
    InstantiateNode = 21
    ProtocolMethod = 20
    LetNode = 19
    DynTestNode = 18
    Global = 0
    Protocol = 1
    Type = 2
    Protocol_Method = 3
    Type_Method = 4
    Attr_Call = 5
    Var_Def = 6
    MethodCallWithExpressionNode = 7
    MethodCallWithIdentifierNode = 8
    DestructionAssignmentWithAttributeCallExpression = 9
    DestructionAssignmentBasicExpression = 10
    Function = 11
    Assign = 12
    FunctionCall = 13
    BINARY_EXPRESSION = 14
    UNARY_EXPRESSION = 15
    LITERAL_EXPRESSION = 16
    ExpressionBlockNode = 17


class Basic_Types(Enum):
    String =1
    Int = 2
    Boolean = 3
    Null = 0
    UNKNOWN = -1