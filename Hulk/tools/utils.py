from cmp.pycompiler import Token


def contains_space(lis: list[Token]):
    """
    True si la lista contien un token space
    """
    for token in lis:
        if token.is_space_token():
            return True
    return False

def contains_token(list:[Token],token_type:str):
    for token in list:
        if token.token_type.Name == token_type:
            return True
    return False