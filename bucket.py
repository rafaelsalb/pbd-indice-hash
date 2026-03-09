class Bucket:
    def __init__(self, fr: int = 4, increase_collisions=None, increase_overflows=None):
        self._items = []
        self._size = fr
        self._overflow = None
        self.increase_collisions = increase_collisions or (lambda: None)
        self.increase_overflows = increase_overflows or (lambda: None)

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
                self.increase_collisions()
                self.increase_overflows()
                self._overflow = Bucket(self._size, self.increase_collisions, self.increase_overflows)
            self._overflow.add(item)

    def is_full(self):
        return len(self._items) >= self._size
