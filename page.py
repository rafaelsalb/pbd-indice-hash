class Page:
    def __init__(self, size, index: int):
        assert size > 0, "Page size must be a positive integer"
        assert index >= 0, "Page index must be a non-negative integer"
        self._size = size
        self._items = []
        self._index = index

    @property
    def items(self):
        return self._items

    @items.setter
    def set_items(self, _):
        raise Exception("Items cannot be set directly")

    @property
    def index(self):
        return self._index

    @property
    def size(self):
        return self._size

    def add(self, item):
        i = len(self._items)
        if i < self._size:
            self._items.append(item)
            return self._index, i
        else:
            raise Exception("Page is full")

    def is_full(self):
        return len(self._items) >= self._size
