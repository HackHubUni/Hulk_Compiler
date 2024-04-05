from Hulk.Semantic_Check.basic_types.semantic_types import *


class NoneType(TypeInfo):
    def __init__(self):
        super().__init__("None")

    def bypass(self):
        return True


class ObjectType(TypeInfo):
    def __init__(self):
        super().__init__("Object")

    def conforms_to(self, other: TypeInfo):
        return False  # All builtin objects conform to Object but object does not conform to any other object

    def bypass(self):
        return True  # All builtin objects conform to Object, so the object type can bypass the conforms check


class NumType(TypeInfo):
    def __init__(self):
        super().__init__("Number")
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = 0
        self.set_parent(ObjectType())

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, NumType)


class StringType(TypeInfo):
    def __init__(self):
        super().__init__("String")
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = ""
        self.set_parent(ObjectType())

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, StringType)


class BoolType(TypeInfo):
    def __init__(self):
        super().__init__("Bool")
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = False
        self.set_parent(ObjectType())

    def __eq__(self, other: TypeInfo):
        return other.name == self.name or isinstance(other, BoolType)


class ErrorType(TypeInfo):
    def __init__(self):
        super().__init__("<error>")
        self.set_parent(ObjectType())  # TODO: This can be removed?

    def bypass(self):
        return True

    def __eq__(self, other: TypeInfo):
        return isinstance(other, TypeInfo)


class VectorType(TypeInfo):
    def __init__(self):
        super().__init__("Vector")
        self.set_constructor_arguments([VariableInfo("vector_type_id", "None")])
        self.attributes["value"] = VariableInfo("value", self.name)
        self.attributes["value"].value = []
        # self.attributes["vector_type_id"]
        self.set_parent(ObjectType())

    def __eq__(self, value: object) -> bool:
        return value.name == self.name or isinstance(value, VectorType)


class RangeType(TypeInfo):
    def __init__(self):
        super().__init__("Range")
        self.set_constructor_arguments(
            [VariableInfo("start", "Number"), VariableInfo("end", "Number")]
        )
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
