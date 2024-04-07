from Hulk.Semantic_Check.type_inference import TypeInference
from Hulk.tools.Ast import *
from Hulk.Semantic_Check.type_collector import TypeCollector
from Hulk.Semantic_Check.type_builder import TypeBuilder
from Hulk.Semantic_Check.basic_types.scopes import *


def check_semantics(ast: AstNode, scope: HulkScopeLinkedNode, errors: list) -> bool:
    """Check the semantics of the Ast tree"""
    type_collector: TypeCollector = TypeCollector(scope, errors)
    type_collector.visit(ast, scope)

    type_builder: TypeBuilder = TypeBuilder(scope, errors)
    type_builder.visit(ast, scope)

    type_inference= TypeInference(scope, errors)
    type_inference.visit(ast, scope)

    return len(errors) == 0
