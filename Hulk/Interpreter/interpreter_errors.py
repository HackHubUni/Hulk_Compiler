
class InterpreterError(Exception):
    @property
    def text(self):
        return self.args[0]