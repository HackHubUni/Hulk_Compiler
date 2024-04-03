from semantic_types import *


class ObjectType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "Object")


class NoneType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "None")


class NumType(ObjectType):
    def __init__(self):
        TypeInfo.__init__(self, "Number")
        self.attributes["value"] = VariableInfo("value", self.name)

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, NumType)


class StringType(ObjectType):
    def __init__(self):
        TypeInfo.__init__(self, "String")
        self.attributes["value"] = VariableInfo("value", self.name)

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, StringType)


class BoolType(ObjectType):
    def __init__(self):
        TypeInfo.__init__(self, "Bool")
        self.attributes["value"] = VariableInfo("value", self.name)

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, BoolType)


class ErrorType(TypeInfo):
    def __init__(self):
        TypeInfo.__init__(self, "<error>")

    def conforms_to(self, other: TypeInfo):
        return True

    def bypass(self):
        return True

    def __eq__(self, other: TypeInfo):
        return isinstance(other, TypeInfo)
