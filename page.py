class Page:
    def __init__(self, size):
        self._size = size
        self._items = []

    @property
    def items(self):
        return self._items

    @items.setter
    def set_items(self, _):
        raise Exception("Items cannot be set directly")

    def add(self, item):
        if len(self._items) < self._size:
            self._items.append(item)
        else:
            raise Exception("Page is full")

    def is_full(self):
        return len(self._items) >= self._size
