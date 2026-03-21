class UpperAttr(type):
    def __new__(cls, name, base,dct):
        uppr = {}
        for attr, val in dct.items():
            if not attr.startswith("__"):
                uppr[attr.upper()] = val
            else:
                uppr[attr] = val

        return super().__new__(cls,name, base, uppr)

class Demo(metaclass=UpperAttr):
    a = "check"

a1 = Demo()
print(hasattr(Demo, "a"))
print(hasattr(Demo, "A"))
#print(a1.a)
print(a1.A)