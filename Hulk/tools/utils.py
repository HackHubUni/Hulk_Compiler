from cmp.pycompiler import Token


def contains_space(lis: list[Token]):
    """
    True si la lista contien un token space
    """
    for token in lis:
        if token.is_space_token():
            return True
    return False
