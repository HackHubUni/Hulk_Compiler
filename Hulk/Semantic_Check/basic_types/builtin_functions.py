from Hulk.Semantic_Check.basic_types.instance_types import VariableInfo, TypeInstance
from Hulk.tools.Ast import FunctionDeclarationNode
from Hulk.Semantic_Check.basic_types.semantic_types import FunctionInfo

# from builtin_protocols import *
import math
from random import random


class BuiltinFunction(FunctionInfo):
    def __init__(
            self,
            name: str,
            param_names: list[VariableInfo],
            return_type: str,
            function_pointer: FunctionDeclarationNode,
    ):
        super().__init__(name, param_names, return_type, function_pointer)

    def result(self):
        """This function returns the result of the function.
        All builtin functions must implement this method"""
        pass


class SinFunction(BuiltinFunction):
    """This Builtin Function computes the sin of a number"""

    def __init__(self):
        super().__init__("sin", [VariableInfo("x", "Number")], "Number", None)

    def result(self):
        # Calculate the sin of the value
        argument: VariableInfo = self.arguments[0]
        value:TypeInstance=argument.value
        result = VariableInfo("result", "Number")
        result.value = math.sin(value)
        return result


class CosFunction(BuiltinFunction):
    """This Builtin Function computes the cos of a number"""

    def __init__(self):
        super().__init__("cos", [VariableInfo("x", "Number")], "Number", None)

    def result(self):
        # Calculate the cos of the value
        argument = self.arguments[0].value
        result = VariableInfo("result", "Number")
        result.value = math.cos(argument.value)
        return result


class SqrtFunction(BuiltinFunction):
    """This Builtin Function computes the sqrt of a number"""

    def __init__(self):
        super().__init__("sqrt", [VariableInfo("x", "Number")], "Number", None)

    def result(self):
        # Calculate the sqrt of the value
        argument = self.arguments[0].value
        result = VariableInfo("result", "Number")
        result.value = math.sqrt(argument.value)
        return result


class LogFunction(BuiltinFunction):
    """This Builtin Function computes the log of a number in a base"""

    def __init__(self):
        super().__init__(
            "log",
            [VariableInfo("base", "Number"), VariableInfo("value", "Number")],
            "Number",
            None,
        )

    def result(self):
        # Calculate the log in a base of a value
        base = self.arguments[0].value
        value = self.arguments[1].value
        result = VariableInfo("result", "Number")
        result.value = math.log(value.value, base.value)
        return result


class ExponentialFunction(BuiltinFunction):
    """This Builtin Function computes the exponential of a number"""

    def __init__(self):
        super().__init__("exp", [VariableInfo("x", "Number")], "Number", None)

    def result(self):
        # Calculate the exponential of the value
        argument = self.arguments[0].value
        result = VariableInfo("result", "Number")
        result.value = math.exp(argument.value)
        return result


class RandomFunction(BuiltinFunction):
    """This Builtin Function generates a random number between 0 and 1"""

    def __init__(self):
        super().__init__("random", [], "Number", None)

    def result(self):
        # Generate a random number between 0 and 1
        result = VariableInfo("result", "Number")
        result.value = random()
        return result



class PrintFunction(BuiltinFunction):
    """This Builtin Function prints a value"""

    def __init__(self):
        super().__init__("print", [VariableInfo("x", "Object")], "String", None)

    def result(self):
        # Print the value
        argument = self.arguments[0].value
        print(argument.value)
        return None


builtin_functions: list[str] = [
    SinFunction().name,
    CosFunction().name,
    SqrtFunction().name,
    LogFunction().name,
    ExponentialFunction().name,
    RandomFunction().name,
    PrintFunction().name
]
