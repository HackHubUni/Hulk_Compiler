from instance_types import VariableInfo
from Hulk.tools.Ast import MethodNode
from semantic_types import MethodInfoBase, TypeMethodInfo

class BuiltinMethod(MethodInfoBase):
    def __init__(self, name: str, arguments: list[VariableInfo], return_type: str):
        super().__init__(name, arguments, return_type)

class VectorAddMethod(BuiltinMethod):
    def __init__(self):
        super().__init__("add", [VariableInfo("element", "Vector")], "Vector")