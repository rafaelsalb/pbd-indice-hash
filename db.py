from config import BUCKET_SIZE, BUCKET_COUNT, PAGE_SIZE, PAGE_COUNT, REG_COUNT
from index import Index
from words import WORDS


class Database:
    def __init__(self, n_buckets: int = BUCKET_COUNT, bucket_size: int = BUCKET_SIZE, n_pages: int = PAGE_COUNT, page_size: int = PAGE_SIZE):
        self._index = Index(n_buckets, bucket_size, n_pages, page_size, self.increase_collisions, self.increase_overflows)
        self._collisions = 0
        self._overflows = 0

    @property
    def index(self):
        return self._index

    @property
    def collisions(self):
        return self._collisions

    @collisions.setter
    def set_collisions(self, value):
        self._collisions = value

    @property
    def overflows(self):
        return self._overflows

    @overflows.setter
    def set_overflows(self, value):
        self._overflows = value

    def increase_collisions(self):
        self._collisions += 1

    def increase_overflows(self):
        self._overflows += 1


if __name__ == "__main__":
    db = Database()
    db.index.fill(WORDS)
    print(f"Collisions: {db.collisions}")
    print(f"Overflows: {db.overflows}")
