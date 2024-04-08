from Hulk.Semantic_Check.basic_types.builtin_types import *
from Hulk.tools.Ast import *


def fix_var_def_node(var_def: VarDefNode) -> VarDefNode:
    """Fix the AST node of the VarDefNode. If the var_type is None then it set it to 'None'"""
    var_type = var_def.var_type
    if var_type is None or var_type.isspace():
        var_def.var_type = NoneType.static_name()
    return var_def


def fix_parent_type_id(type_declaration: TypeDeclarationNode):
    """Fix the AST node of the TypeDeclarationNode. If the parent_type is None then it set it to 'Object'"""
    parent_type = type_declaration.parent_type_id
    if parent_type is None or parent_type.isspace():
        type_declaration.parent_type_id = ObjectType.static_name()
    return type_declaration


def fix_method_return_type(method_def: MethodNode) -> MethodNode:
    """Fix the AST node of the MethodNode. If the return_type is None then it set it to 'None'"""
    return_type = method_def.return_type
    if return_type is None or return_type.isspace():
        method_def.return_type = NoneType.static_name()
    return method_def


def fix_function_return_type(
    function_def: FunctionDeclarationNode,
) -> FunctionDeclarationNode:
    """Fix the AST node of the FunctionDeclarationNode. If the return_type is None then it set it to 'None'"""
    return_type = function_def.return_type
    if return_type is None or return_type.isspace():
        function_def.return_type = NoneType.static_name()
    return function_def


def get_variable_info_from_var_def(var_def: VarDefNode) -> VariableInfo:
    """Returns a VariableInfo from a VarDefNode.
    This function also fix the type of the VarDefNode to a valid type"""
    fix_var_def_node(var_def)
    return VariableInfo(var_def.var_name, var_def.var_type)


def get_variable_info_from_var_assign(var_assign: AssignNode) -> VariableInfo:
    """Returns a VariableInfo from a AssignNode"""
    return get_variable_info_from_var_def(var_assign.var_definition)
