import uuid


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]


def get_unique_name_with_guid(name: str):
    """This function returns a new TypeName with a GUID added to the end"""
    guid = str(uuid.uuid4())
    return f"{name}_{guid}"
