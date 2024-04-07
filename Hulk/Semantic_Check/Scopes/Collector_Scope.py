
from Hulk.tools.Ast import *
from Hulk.tools.Ast import *
from Hulk.Semantic_Check.to_replace.type_node import *
from typing import Self
import copy
from Hulk.Semantic_Check.basic_types.Tags.tags import *
from enum import Enum
import uuid


class Unary_Container:

    def __init__(self, unary: UnaryExpressionNode,):
        self.unary = unary
        self.is_literal=self.get_literal_Type_()
        self.is_var=self.is_var_()
        self.is_Not=self.is_Not_()
        self.is_negative=self.is_negative_()




    def is_Not_(self)->bool:
       if isinstance(self.unary,NotNode):
           return  True
       return False


    def get_literal_Type_(self)->Basic_Types:
        """
        Si es un literal devuelve el tipo basico sino uknown
        """
        if isinstance(self.unary, LiteralExpressionNode):
            if isinstance(self.unary, LiteralBoolNode):
                return  Basic_Types.Boolean
            elif isinstance(self.unary, LiteralNumNode):
                return  Basic_Types.Int
            elif isinstance(self.unary, LiteralStrNode):
                return  Basic_Types.String
        else:
                return Basic_Types.UNKNOWN

    def is_var_(self)->bool:
        if isinstance(self.unary, VarNode):
            return  True
        return False
    def is_negative_(self)->bool:
        if isinstance(self.unary, NegativeNode):
            return  True
        return False


    # Agrega más tags según sea necesario


class HulkScope:
    def __init__(self, father: Self, name: str, tag: TagsEnum):

        self.name: str = name
        # Chequear que el array no sea nulo o vacio
        if name is None or name == "":
            self.name = f' guid: {str(uuid.uuid4())}'
        self.tag = tag
        self.father: HulkScope = father
        self.decla_parents: ProtocolDeclarationNode | ProtocolMethodNode | TypeDeclarationNode | MethodNode = None
        self.childs: list[HulkScope] = []
        self.functions_decl: dict[str, FunctionDeclarationNode] = {}
        self.functions_call: dict[str, list[FunctionCallNode]] = {}
        self.attr_: dict[str, AttrCallNode] = {}
        # Types Zone
        self.type_id_str = ""
        self.types_methods: dict[str, MethodNode] = {}
        self.inherence_methods: dict[str, MethodNode] = {}
        self.override_methods: dict[str, MethodNode] = {}
        self.methods_call: dict[str, list[MethodCallNode]] = {}
        # Protocols Zone
        self.protocols_methods: dict[str, ProtocolMethodNode] = {}
        self.procotocols_inherence_methods: dict[str, ProtocolMethodNode] = {}

        self.args_: dict[str, VarDefNode] = {}
        #Para conocer el valor que tengo


        # Numero para indexar
        self.index_value_for_indexing: int = -2
        # Referencia al tipo que pertenece esto si no esta declarado
        self.Type_Var=TagsEnum.Null


        #Unary_Types
        self.unary_value: Unary_Container = None

        #para el let
        self.let_: dict[str, LetNode] = {}


    def get_scope_child_(self, name: str, tag: TagsEnum) -> Self:
        # new = copy.deepcopy(self)
        # new.father = father
        # new.tag = tag
        # new.name = name
        new = HulkScope(self, name, tag)
        self.childs.append(new)

        return new

    def set_assign_(self, assign: AssignNode):
        name = assign.var.id
        if name in self.args_:
            raise SemanticError(f'No se puede asignar dos veces a la variable  {name}')
        # La variable a la cual se asigna
        self.args_[name] = assign.var

    def set_decla_father_(self, decla: ProtocolDeclarationNode | ProtocolMethodNode | TypeDeclarationNode | MethodNode):
        if self.decla_parents is not None:
            raise SemanticError('No se puede tener dos prototipos o types con el mismo nombre')
        self.decla_parents = decla

    def set_functions_decl_(self, funct_decl: FunctionDeclarationNode):
        name = funct_decl.id
        if name in self.functions_decl:
            raise SemanticError(f'No se puede tener dos funciones con el mismo nombre {name}')
        self.functions_decl[name] = funct_decl

    def set_functions_call_(self, func_call: FunctionCallNode):
        name = func_call.id
        if not name in self.functions_call:
            self.functions_call[name] = [func_call]
        else:
            self.functions_call[name].append(func_call)

    def set_inherence_methods_(self, method: MethodNode):
        name = method.id
        if name in self.inherence_methods:
            raise SemanticError(f'No se puede tener dos metodos con el mismo nombre {name}')
        self.inherence_methods[name] = method

    def set_override_methods_(self, method: MethodNode):
        name = method.id
        if name in self.override_methods:
            raise SemanticError(f'No se puede tener dos metodos con el mismo nombre {name}')
        self.override_methods[name] = method

    def set_types_methods_(self, method: MethodNode):
        name = method.id
        if name in self.types_methods:
            raise SemanticError(f'No se puede tener dos metodos con el mismo nombre {name}')
        self.types_methods[name] = method

    def set_methods_call_(self, func_call: MethodCallNode):
        name = func_call.method_id
        if not name in self.methods_call:
            self.methods_call[name] = [func_call]
        else:
            self.methods_call[name].append(func_call)

    def set_protocol_methods_(self, method: ProtocolMethodNode):
        name = method.id
        if name in self.protocols_methods:
            raise SemanticError(f'No se puede tener dos metodos con el mismo nombre {name}')
        self.protocols_methods[name] = method

    def set_attr_(self, attr: AttrCallNode):
        name = attr.variable_id
        if name in self.attr_:
            raise SemanticError(f'No se puede tener dos atributos con el mismo nombre {name}')
        self.attr_[name] = attr

    def set_arg(self, arg: VarDefNode):
        """
        Set un argumento en el scope
        """
        name = arg.id
        if name in self.args_:
            raise SemanticError(f'No se puede tener dos argumentos con el mismo nombre {name}')
        self.args_[name] = arg

    def set_args_(self, args: list[VarDefNode]):
        """
        Set una lista de argumentos en el scope
        """
        for arg in args:
            self.set_arg(arg)

    def set_let(self, let: LetNode):
        assig_list = let.assign_list

        for assig in assig_list:
            self.set_assign_(assig)

    def set_instantiate(self, instantiate: InstantiateNode):
        name = instantiate.type_id
        if self.type_id_str != "":
            raise SemanticError(f'Error para instanciar {name}')
        self.type_id_str = name

    def set_downcast(self, downcast: DowncastNode):
        name = downcast.type
        if self.type_id_str != "":
            raise SemanticError(f'Error para castear {name}')
        self.type_id_str = name

    def set_indexing(self, indexing: IndexingNode):
        index = indexing.index
        if index.isdigit():
            index = int(index)
            if index < 0:
                raise SemanticError(f'Error para indexar {index} tiene que ser positivo')
            self.index_value_for_indexing = index

    def set_Unary(self, unary:UnaryExpressionNode):
        self.unary_value = Unary_Container(unary)






    #def set_literal(self, literal: LiteralExpressionNode):
    #    self.value = literal
class Collector_Info(HulkScope):
    def __init__(self):
        super().__init__(father=None, tag=TagsEnum.Global, name="Base_Scope")
        self.protocols_: dict[str, HulkScope] = {}
        self.prot_info_: dict[str, HulkScope] = {}
        self.types_: dict[str, HulkScope] = {}
        self.functions_decl_: dict[str, HulkScope] = {}
        self.protocols_methods: dict[str, ProtocolMethodNode] = {}


    def __get_new_child_scope(self, name: str, father: HulkScope, tag: TagsEnum) -> HulkScope:
        new_scope = HulkScope(name=name, father=father, tag=tag)
        self.childs.append(new_scope)
        return new_scope

    def add_protocol(self, prot_decl: ProtocolDeclarationNode) -> HulkScope:
        name = prot_decl.id
        if name in self.protocols_:
            raise SemanticError(f'No pueden existir dos protocolos con igual nombre {name}')
        scope = self.__get_new_child_scope(name, self, TagsEnum.Protocol)
        self.protocols_[name] = scope
        return scope

    def add_procols_methods(self, prot_method: ProtocolMethodNode, scope: HulkScope):
        """
        Desde el contexto global se añade un nuevo metodo de protocolo
        """
        name = prot_method.id
        if name in self.protocols_methods:
            raise SemanticError(f'No pueden existir dos métodos de procolos con el mismo nombre {name}')
        self.protocols_methods[name] = prot_method

        new_scope = scope.get_scope_child_(name, TagsEnum.ProtocolMethod)
        new_scope.set_protocol_methods_(prot_method)
        return new_scope

    # Type Zone

    def add_type(self, type_decl: TypeDeclarationNode):
        name = type_decl.id
        if name in self.types_:
            raise SemanticError(f'No pueden existir dos types con igual nombre {name}')
        scope = self.__get_new_child_scope(name, self, TagsEnum.Type)
        scope.set_args_(type_decl.args)
        self.types_[name] = scope

        return scope

    def add_function_declaration(self, func_decl: FunctionDeclarationNode) -> HulkScope:
        name = func_decl.id
        if name in self.functions_decl_:
            raise SemanticError(f'No pueden existir dos funciones con igual nombre {name}')
        scope = self.__get_new_child_scope(name, self, TagsEnum.Function)
        self.functions_decl_[name] = scope
        return scope

    def add_function_call(self, func_call: FunctionCallNode, local_scope: HulkScope) -> HulkScope:
        name = func_call.id
        scope = local_scope.get_scope_child_(name, TagsEnum.FunctionCall)
        scope.set_functions_call_(func_call)
        return scope

    def add_type_methods(self, type_method: MethodNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo metodo de type
        """
        name = type_method.id
        new_scope = scope.get_scope_child_(name, TagsEnum.Type_Method)
        new_scope.set_types_methods_(type_method)
        return new_scope

    def add_call_attr(self, attr_call: AttrCallNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo attr call
        """
        name = attr_call.variable_id
        new_scope = scope.get_scope_child_(name, TagsEnum.Attr_Call)
        new_scope.set_attr_(attr_call)
        return new_scope

    def add_call_methods(self, func_call: MethodCallNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo method call
        """
        name = func_call.method_id
        tags = TagsEnum.MethodCallWithExpressionNode if isinstance(func_call,
                                                                   MethodCallWithExpressionNode) else TagsEnum.MethodCallWithIdentifierNode
        new_scope = scope.get_scope_child_(name, tags)
        new_scope.set_methods_call_(func_call)
        return new_scope

    def add_assign(self, assign: AssignNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo assign
        """
        name = assign.var.id
        new_scope = scope.get_scope_child_(name, TagsEnum.Assign)

        new_scope.set_assign_(assign)
        return new_scope

    def add_var_def(self, type_method: VarDefNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo var def
        """
        name = type_method.id

        new_scope = scope.get_scope_child_(name, TagsEnum.Var_Def)
        new_scope.set_arg(type_method)
        return new_scope

    # Destrucccion Assignment Zone
    def add_destruction_assignment_with_attribute_call(self,
                                                       destruccion_with_attr: DestructionAssignmentWithAttributeCallExpression,
                                                       scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo attr call
        """
        name = destruccion_with_attr.attribute_call_expression.variable_id
        new_scope = scope.get_scope_child_(name, TagsEnum.DestructionAssignmentWithAttributeCallExpression)

        return new_scope

    def add_destruction_assignment_basic(self, destruccion_basic: DestructionAssignmentBasicExpression,
                                         scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo attr call
        """
        name = destruccion_basic.id
        new_scope = scope.get_scope_child_(name, TagsEnum.DestructionAssignmentBasicExpression)

        return new_scope

    def add_binary_expression(self, binary_expr: BinaryExpressionNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo BinaryExpression
        """

        new_scope = scope.get_scope_child_("", TagsEnum.BINARY_EXPRESSION)

        return new_scope

    def add_unary_expression(self, unary_expr: UnaryExpressionNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo UnaryExpression
        """

        new_scope = scope.get_scope_child_(f"Unary: {unary_expr.value}", TagsEnum.UNARY_EXPRESSION)
        new_scope.set_Unary(unary_expr)

        return new_scope

   #def add_literal_expression(self, literal_expr: LiteralExpressionNode, scope: HulkScope) -> HulkScope:
   #    """
   #    Desde el contexto global se añade un nuevo LiteralExpression
   #    """

   #    new_scope = scope.get_scope_child_("", TagsEnum.LITERAL_EXPRESSION)

   #    return new_scope

    def add_expression_block(self, expr_block: ExpressionBlockNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo ExpressionBlock
        """

        new_scope = scope.get_scope_child_("", TagsEnum.ExpressionBlockNode)

        return new_scope

    def add_dyn_test(self, dyn_test: DynTestNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo DynTest
        """

        new_scope = scope.get_scope_child_("", TagsEnum.DynTestNode)

        return new_scope

    def add_let(self, let: LetNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo Let
        """
        for ass in let.assign_list:
            name= ass.var.id
            if name in self.let_:
                raise SemanticError(f'No pueden existir dos let con el mismo nombre {name}')
            self.let_[name] = let


        new_scope = scope.get_scope_child_("", TagsEnum.LetNode)

        new_scope.set_let(let)
        return new_scope

    def add_instantiate(self, instantiate: InstantiateNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo Instantiate
        """
        type_name = instantiate.type_id
        new_scope = scope.get_scope_child_(f'instantiate: {type_name}', TagsEnum.InstantiateNode)

        return new_scope

    def add_downcast(self, downcast: DowncastNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo DownCast
        """
        name=downcast.type
        new_scope = scope.get_scope_child_(f'downcast: {name}', TagsEnum.DownCastNode)

        new_scope.set_downcast(downcast)

        return new_scope

    def add_if(self, if_: IfNodeExpression, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo If
        """

        new_scope = scope.get_scope_child_("", TagsEnum.IfNode)

        return new_scope

    def add_elif_atom(self, elif_: ElifNodeAtomExpression, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo elifAtom
        """

        new_scope = scope.get_scope_child_("", TagsEnum.ElifNodeAtom)

        return new_scope

    def add_while(self, while_: WhileExpressionNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo While
        """

        new_scope = scope.get_scope_child_("", TagsEnum.WhileNode)

        return new_scope

    def add_vector(self, vector: VectorNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo Vector
        """

        new_scope = scope.get_scope_child_("", TagsEnum.VectorNode)

        return new_scope

    def add_indexing(self, indexing: IndexingNode, scope: HulkScope) -> HulkScope:
        """
        Desde el contexto global se añade un nuevo Indexing
        """

        new_scope = scope.get_scope_child_("", TagsEnum.IndexingNode)
        new_scope.set_indexing(indexing)
        return new_scope
