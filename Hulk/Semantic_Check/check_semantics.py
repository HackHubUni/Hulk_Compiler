from Hulk.tools.Ast import *
from type_collector import TypeCollector
from type_builder import TypeBuilder
from basic_types.scopes import *


def check_semantics(ast: AstNode, scope: HulkScopeLinkedNode, errors: list) -> bool:
    """Check the semantics of the Ast tree"""
    type_collector: TypeCollector = TypeCollector(scope, errors)
    type_collector.visit(ast)

    type_builder: TypeBuilder = TypeBuilder(scope, errors)
    type_builder.visit(ast)

    return len(errors) == 0
