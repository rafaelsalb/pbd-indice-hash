class Bucket:
    def __init__(self, fr: int = 4):
        self._items = []
        self._size = fr
        self._overflow = None

    @property
    def items(self):
        return self._items

    @property
    def size(self):
        return self._size

    def add(self, item):
        if len(self._items) < self._size:
            self._items.append(item)
        else:
            if self._overflow is None:
                self._overflow = Bucket(self._size)
            self._overflow.add(item)

    def is_full(self):
        return len(self._items) >= self._size
