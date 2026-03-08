class Page:
    def __init__(self, size):
        self._size = size
        self._items = []

    def add(self, item):
        if len(self._items) < self._size:
            self._items.append(item)
        else:
            raise Exception("Page is full")


if __name__ == "__main__":
    pages = [Page(3) for _ in range(2)]

    for i in range(6):
        try:
            pages
