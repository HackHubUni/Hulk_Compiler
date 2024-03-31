from Hulk.Lexer.Hulk_Lexer import get_hulk_lexer

lexer = get_hulk_lexer()

print("Cargado el lexer ")
print(lexer(f"let casa = \"Caca\" "))

def test(token: str, type_token: str):

    a = lexer(token)
    assert str(a[0].token_type) == type_token, f"El token {a[0]} de tipo {a[0].token_type} se esperaba {type_token} "

def testing_ids():
    ids_=["el_glsorwjonerv9495849,personas59,__comomucho,__comoicnru049__"]
    a=0
    for i,val in enumerate(ids_,1):
        test(val,"id")
        a=i
    print(f"Se ejecutaron correctamente {a}")

testing_ids()

