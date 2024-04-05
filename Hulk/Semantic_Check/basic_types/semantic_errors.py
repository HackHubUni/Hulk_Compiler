class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]


def get_name_with_added_error(type_name: str):
    """This function returns a new TypeName with the string '<ERROR>' added to the end"""
    return f"{type_name}<ERROR>"
