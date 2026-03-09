class Page:
    def __init__(self, size):
        self._size = size
        self._items = []

    def add(self, item):
        if len(self._items) < self._size:
            self._items.append(item)
        else:
            raise Exception("Page is full")

    def is_full(self):
        return len(self._items) >= self._size
