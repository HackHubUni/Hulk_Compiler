from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer

lexer = get_hulk_lexer()

print("Cargado el lexer ")
print(lexer(f"let casa = \"Caca\" "))

def test(token: str, type_token: str):

    a = lexer(token)
    assert str(a[0].token_type) == type_token , f"El token {a[0]} de tipo {a[0].token_type} se esperaba {type_token} "
    assert  str(a[-1].token_type)=="$",f"El token {a[-1]} no es del tipo $ es del tipo {a[-1].token_type} "

def testing_ids():
    ids_=[":= ","="]
    tokens=[":=","="]
    a=0
    for i,val in enumerate(ids_,1):
        test(val,tokens[i-1])
        a=i
    print(f"Se ejecutaron correctamente {a}")

#testing_ids()

def test_comments():
    comments_=["//hola","/*hola*/","/*hola \n omiemfir */"]
    tokens=["comments"]
    a=0
    for i,val in enumerate(comments_,1):
        test(val,tokens[0])
        a=i
    print(f"Se ejecutaron correctamente {a}")

def test_strings():
    strings = [f'"hola"', f'" hola \n \t \" "', f' " hola \n omiemfir "']
    tokens = ["string"]
    a = 0
    for i, val in enumerate(strings, 1):
        test(val, tokens[0])
        a = i
    print(f"Se ejecutaron correctamente {a}")
