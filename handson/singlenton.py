

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self):
        #if not hasattr(self, "initialized"):
        self.logs = []
        self.initialized = True
        print("Initialized 1st time")

    def log(self, msg):
        self.logs.append(msg)
        print(f"logged: {msg}")

log1=Logger()

log1.log("1st log")

log2=Logger()
log2.log("2nd log")

print(f"same check: {log1 is log2}")