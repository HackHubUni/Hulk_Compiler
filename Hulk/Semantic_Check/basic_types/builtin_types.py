from Hulk.Semantic_Check.basic_types.semantic_types import *


class NoneType(TypeInfo):
    def __init__(self):
        super().__init__(NoneType.static_name())

    @staticmethod
    def static_name() -> str:
        return "<None>"

    def bypass(self):
        return True


class ErrorType(TypeInfo):
    def __init__(self):
        super().__init__(ErrorType.static_name())

    @staticmethod
    def static_name() -> str:
        return "<Error>"

    def bypass(self):
        return True

    def conforms_to(self, other: TypeInfo) -> bool:
        return True

    def __eq__(self, other: TypeInfo):
        return isinstance(other, TypeInfo)


class ObjectType(TypeInfo):
    def __init__(self):
        super().__init__(ObjectType.static_name())

    @staticmethod
    def static_name() -> str:
        return "Object"

    def conforms_to(self, other: TypeInfo):
        return False  # All builtin objects conform to Object but object does not conform to any other object


class BuiltinType(TypeInfo):
    """From this types is prohibit to inherit"""

    def __init__(self, type_name: str):
        super().__init__(type_name)


class NumType(BuiltinType):
    def __init__(self):
        super().__init__(NumType.static_name())
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = 0
        self.set_parent(ObjectType())

    @staticmethod
    def static_name() -> str:
        return "Number"

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, NumType)


class StringType(BuiltinType):
    def __init__(self):
        super().__init__(StringType.static_name())
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = ""
        self.set_parent(ObjectType())

    @staticmethod
    def static_name() -> str:
        return "String"

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, StringType)


class BoolType(BuiltinType):
    def __init__(self):
        super().__init__(BoolType.static_name())
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = False
        self.set_parent(ObjectType())

    @staticmethod
    def static_name() -> str:
        return "Bool"

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, BoolType)


class VectorType(BuiltinType):
    def __init__(self):
        super().__init__(VectorType.static_name())
        self.set_constructor_arguments([VariableInfo("vector_type_id", "<None>")])
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = []
        # self.attributes["vector_type_id"]
        self.set_parent(ObjectType())

    @staticmethod
    def static_name() -> str:
        return "Vector"

    def __eq__(self, value: object) -> bool:
        return value.name == self.name or isinstance(value, VectorType)


class RangeType(BuiltinType):
    def __init__(self):
        super().__init__(RangeType.static_name())
        self.set_constructor_arguments(
            [VariableInfo("start", "Number"), VariableInfo("end", "Number")]
        )
        self.set_parent(ObjectType())

    @staticmethod
    def static_name() -> str:
        return "Range"


def is_builtin_type(type_info: TypeInfo) -> bool:
    """Returns true if the type is a builtin type.
    No single new type definition is allowed to inherit from a builtin type."""
    return isinstance(type_info, BuiltinType)


def is_type_name_prohibit(type_name: str) -> bool:
    """Says if the type name could be used as a type definition name"""
    return type_name in [
        NoneType.static_name(),
        ErrorType.static_name(),
        ObjectType.static_name(),
        NumType.static_name(),
        StringType.static_name(),
        BoolType.static_name(),
        VectorType.static_name(),
        RangeType.static_name(),
    ]


builtin_types: list[str] = [
    NoneType().name,
    ObjectType().name,
    NumType().name,
    StringType().name,
    BoolType().name,
    ErrorType().name,
    VectorType().name,
]
