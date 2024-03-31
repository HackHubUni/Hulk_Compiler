from Lexer_Parser.Lexer.lexer import Lexer

from cmp.pycompiler import Grammar

class Regex_Utils:
    def __init__(self):
        self.letters_ = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
        self.uppercase_letters_ = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
        self.all_symbols_ = '|'.join(chr(n) for n in range(255) if not n in [ord('\\'), ord('|'), ord('*'), ord('ε'), ord('('), ord(')'), ord('\n'), ord('"')])
        self.escaped_regex_operations_ = '|'.join(s for s in "\| \* \( \) \ε".split())
        self.nonzero_digits_ = '|'.join(str(n) for n in range(1, 10))
        self.letters_ = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
        self.uppercase_letters_ = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
        self.valid_string_symbols_ = '|'.join(c for c in " : ; , . _ - \+ '  /  ^ % & ! = < > \\( \\) { } [ ] @ ".split()) #
        self.valid_id_symbols_ = '_'
        self.delim_ = ' |\t|\n'
        self.natural_numbers_ = f'({self.nonzero_digits_})({self.nonzero_digits_}|0)*'
        self.natural_aster_numbers_ = f'({self.natural_numbers_})|0'
        self.floating_point_numbers_ = f'({self.natural_aster_numbers_}).(({self.natural_aster_numbers_})({self.natural_aster_numbers_})*)'
        self.delim_ = ' |\t|\n'

        self.string=f'"({self.letters_}|{self.uppercase_letters_}|0|{self.nonzero_digits_}|{self.valid_string_symbols_}|\t| |\|| |\\\\")*"'

        self.type_id=f'({self.uppercase_letters_})({self.letters_}|{self.uppercase_letters_}|0|{self.nonzero_digits_}|{self.valid_id_symbols_})*'
#a=Regex_Utils()


G=Grammar()
ru=Regex_Utils()
string=G.Terminal("string")
a=[(string,ru.string)]

print(ru.valid_string_symbols_)
lexer=Lexer(a,G.EOF)

print(lexer("\"It's bird!\""))