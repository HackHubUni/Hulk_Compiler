from semantic_types import *


class NoneType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "None")


class ObjectType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "Object")

    def conforms_to(self, other: TypeInfo):
        return True  # All builtin objects conform to Object

    def bypass(self):
        return True  # All builtin objects conform to Object, so the object type can bypass the conforms check


class NumType(TypeInfo):
    def __init__(self):
        super().__init__(self, "Number")
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = 0
        self.set_parent(ObjectType())

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, NumType)


class StringType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "String")
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = ""
        self.set_parent(ObjectType())

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, StringType)


class BoolType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "Bool")
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = False
        self.set_parent(ObjectType())

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, BoolType)


class ErrorType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "<error>")
        self.set_parent(ObjectType())

    def conforms_to(self, other: TypeInfo):
        return True

    def bypass(self):
        return True

    def __eq__(self, other: TypeInfo):
        return isinstance(other, TypeInfo)


class VectorType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "Vector", [VariableInfo("vector_type_id", "String")])
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = []
        self.attributes["vector_type_id"]
        self.set_parent(ObjectType())

    def __eq__(self, value: object) -> bool:
        return value.name == self.name or isinstance(value, VectorType)


class RangeType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "Range")
        self.set_parent(ObjectType())


builtin_types: list[str] = [
    NoneType().name,
    ObjectType().name,
    NumType().name,
    StringType().name,
    BoolType().name,
    ErrorType().name,
    VectorType().name,
]
