class InitInjection(type):
    def __new__(cls, name, base, dct):
        if not "__init__" in dct:
            def __init__(self, *val):
                self.val = val
            dct["__init__"] = __init__
        return super().__new__(cls, name, base, dct)

class Check(metaclass=InitInjection):
    def show(self):
        print(self.val)

c=Check(42)

c.show()

