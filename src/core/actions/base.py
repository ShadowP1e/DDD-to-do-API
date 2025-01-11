class BaseAction:
    def to_dict(self):
        _dict = self.__dict__.copy()
        return _dict
