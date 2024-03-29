from Hulk.Grammar.gramarlr1 import Gramarlr1
from cmp.pycompiler import Terminal

# Get the Hulk Grammar
gramar = Gramarlr1()
# Get the Terminals
s = gramar.Grammar.Get_Terminal


def get_normal_regex(normal_regex: str):
    """
    Splits the given `normal_regex` string into a list of individual regex patterns.

    Args:
        normal_regex (str): The string containing the normal regex patterns.

    Returns:
        List[Tuple[Terminal, str]]: A list of tuples, where each tuple contains a `Terminal` object and the corresponding regex pattern.
    """
    lis = normal_regex.split()
    hulk_regex: [(Terminal, str)] = [(s(val), val) for val in lis]
    return hulk_regex


# normal Regex las que sus regex son iguales a ellas

normal_regex = " { } [ ]  ; :  , . ( ) || let in  = :=   "  #
normal_regex += " if else elif while for function "
normal_regex += " <= < == >= > != "
normal_regex += " sqrt cos sin expon log rand "
normal_regex += " + - * / % ^ num ! & | "
normal_regex += " type new inherits is as "
normal_regex += " protocol extends "
normal_regex += " true false "
normal_regex += " @ @@ "
normal_regex += " bool  base "

# the result
regex_list: [(Terminal, str)] = get_normal_regex(normal_regex)

assert not " " in regex_list, "Existes espacios en blanco como regex "


#TODO:Arreglar esto despues de añadir cambio, hay que arreglar el parseador de [] para regex, tiene error en las producciones del LL1 para ello sustituir por versiones iniciales
"""
# str
str_ = s("str")
str_regex = "\"((\\\\\")|(\\A))*\""
regex_list.append((str_, str_regex))
# string
string = s("string")
regex_list.append((string, str_regex))
# Id
id_ = s("id")
id_regex = "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"
regex_list.append((id_, id_regex))
# number
number = s("int")
regex_list.append((number, "([0..9]+\.)?[0..9]+"))
"""
def Get_Hulk_Regex():
    """
    Retorna las Regex del Hulk además del EOF de la gramática
    """
    return regex_list, gramar.EOF
