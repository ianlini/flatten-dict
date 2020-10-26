class KeyType:
    pass


class ListIndex(KeyType):
    def __init__(self, index):
        assert isinstance(index, int)
        self.index = index

    def __int__(self):
        return self.index
