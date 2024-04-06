from Hulk.tools.Ast import ProtocolDeclarationNode, ProtocolMethodNode
from Hulk.Semantic_Check.basic_types.semantic_types import *
from Hulk.Semantic_Check.basic_types.builtin_types import *


class BuiltinProtocols(ProtocolInfo):
    def __init__(
        self,
        name: str,
        methods: list[MethodInfoBase],
        parent: Self = None,
    ):
        # super().__init__(name, methods, parent)
        super().__init__(name)
        self.methods = {method.name: method for method in methods}
        self.parent = parent


class IterableProtocol(BuiltinProtocols):
    def __init__(self):
        super().__init__(
            "Iterable",
            [
                MethodInfoBase("next", [], BoolType.static_name()),
                MethodInfoBase("current", [], ObjectType.static_name()),
            ],
        )


builtin_protocols = [IterableProtocol().name]
