from semantic_errors import *
from typing import Self


class VariableInfo:
    def __init__(self, name: str, variable_type: str = None):
        self.name: str = name
        """This is the name of the variable"""
        self.type: str = variable_type
        """This is the name of the type of the variable. Could be None"""
        self.value: TypeInstance = None
        """The value of the variable. Is an instance type. Could be None"""

    def clone(self) -> Self:
        """Returns a Clone of this VariableInfo"""
        return VariableInfo(self.name, self.type)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, VariableInfo):
            return False
        return __value.name == self.name and __value.type == self.type

    def __str__(self):
        return f"{self.name}:{self.type} = {str(self.value)}"

    def __repr__(self):
        return str(self)


class TypeInstance:
    """This class represents an instance of a Type"""

    def __init__(
        self,
        type_id: str,
        variables: list[VariableInfo],
        parent_instance: Self = None,
    ):  # TODO: Add the parent instance as an argument when creating the type
        self.type_id: str = type_id
        """The name of the type"""
        self.variables: dict[str, VariableInfo] = {
            variable.name: variable for variable in variables
        }
        """A dictionary with the names of the variables as key and the VariableInfo type as value"""
        self.parent_instance: Self = parent_instance
        """This is a pointer to the instance of the parent of this instance. Could be None"""

    def get_variables(self) -> list[VariableInfo]:
        """Returns a list with the variables"""
        return list(item[1] for item in self.variables.items())

    def get_type_id(self) -> str:
        """Returns the type id of this instance"""
        return self.type_id

    def get_parent_instance(self) -> Self:
        """Returns a pointer to the parent instance"""
        return self.parent_instance
