class Test:
    def __init__(self) -> None:
        pass


p = Test()


print(p.__getattribute__('__init__'))