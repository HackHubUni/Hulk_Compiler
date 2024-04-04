from Hulk.tools.Ast import ProtocolDeclarationNode, ProtocolMethodNode
from semantic_types import *


class BuiltinProtocols(ProtocolInfo):
    def __init__(
        self,
        name: str,
        methods: list[MethodInfoBase],
        parent: Self = None,
    ):
        super().__init__(name, methods, parent)


class IterableProtocol(BuiltinProtocols):
    def __init__(self):
        super().__init__(
            "Iterable",
            [
                MethodInfoBase("next", [], "Bool"),
                MethodInfoBase("current", [], "Object"),
            ],
        )
