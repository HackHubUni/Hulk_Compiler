from semantic_errors import *
from typing import Self


class VariableInfo:
    def __init__(self, name: str, variable_type: str = None):
        self.name: str = name
        """This is the name of the variable"""
        self.type: str = variable_type
        """This is the name of the type of the variable. Could be None"""
        self.value: InstanceType = None
        """The value of the variable. Could be None"""

    def clone(self) -> Self:
        """Returns a Clone of this VariableInfo"""
        return VariableInfo(self.name, self.type)

    def set_type(self, new_type: str):
        """Sets the type of the Variable if there is no other assigned. In other case is a Semantic Error"""
        if self.type == None or self.type == "":
            self.type = new_type
        else:
            raise SemanticError(
                f'The variable {self.name} is of type "{self.type}" and is receiving a value of type "{new_type}"'
            )

    def set_value_and_type(self, value, new_type):
        pass

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, VariableInfo):
            return False
        return __value.name == self.name and __value.type == self.value

    def __str__(self):
        return f"La variable de tipo {isinstance(self.type)}, con nombre {self.name}"

    def __repr__(self):
        return str(self)


class InstanceType:
    """This class represents an instance of a Type"""

    def __init__(
        self, type_id: str, variables: list[VariableInfo]
    ):  # TODO: Add the parent instance as an argument when creating the type
        self.type_id: str = type_id
        """The name of the type"""
        self.variables: dict[str, VariableInfo] = {
            variable.name: variable for variable in variables
        }
        """A dictionary with the names of the variables as key and the VariableInfo type as value"""
