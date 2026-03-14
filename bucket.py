class Bucket:
    def __init__(self, fr: int = 4, increase_collisions=None, increase_overflows=None, is_overflow=False):
        self._items = []
        self._size = fr
        self._is_overflow = is_overflow
        self._overflow = None
        self.increase_collisions = increase_collisions
        self.increase_overflows = increase_overflows

    @property
    def items(self):
        return self._items

    @property
    def size(self):
        return self._size

    @property
    def is_overflow(self):
        return self._is_overflow

    @is_overflow.setter
    def is_overflow(self, _):
        raise Exception("is_overflow cannot be set directly")

    def add(self, reg, page_address: tuple[int, int]):
        if len(self._items) < self._size:
            if self.is_overflow:
                self.increase_collisions()
            self._items.append((reg, page_address))
        else:
            if self._overflow is None:
                self.increase_overflows()
                self._overflow = Bucket(self._size, self.increase_collisions, self.increase_overflows, True)
            self._overflow.add(reg, page_address)

    def is_full(self):
        return len(self._items) >= self._size

    def search(self, reg):
        print(f"Searching for record '{reg}' in bucket with items {[item for item, _ in self._items]}")
        for i, (r, (page_index, record_index)) in enumerate(self._items):
            print(f"Checking record '{r}' against '{reg}'")
            if r == reg:
                print(f"Record '{reg}' found with page address ({page_index}, {record_index})")
                return i, (page_index, record_index)
        if self._overflow is not None:
            return self._overflow.search(reg)
        return -1, -1
