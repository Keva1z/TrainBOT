

class UNIT():
        def __init__(self, name) -> None:
            self.name = name
            self.count = 0
            
        def __repr__(self) -> str:
            return f"reward({self.name}, {self.count})"