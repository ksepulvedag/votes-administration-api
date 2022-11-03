from abc import ABCMeta


class AbstractModel(metaclass=ABCMeta):
    
    # Construcctor de la clase
    def __init__(self,data):
        for key, value in data.items():
            setattr(self, key, value)