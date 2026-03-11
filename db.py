import time

from config import BUCKET_SIZE, PAGE_SIZE, REG_COUNT
from index import Index
from page import Page
from words import WORDS


class Database:
    def __init__(self, bucket_size: int = BUCKET_SIZE, page_size: int = PAGE_SIZE):
        assert not bucket_size is None and bucket_size > 0, "Bucket size must be a positive integer"
        assert not page_size is None and page_size > 0, "Page size must be a positive integer"
        self._bucket_size = bucket_size
        self._page_size = page_size
        self._n_buckets = 1 + (REG_COUNT // bucket_size)
        self._n_pages = 1 + (REG_COUNT // page_size)
        self._index = Index(self._n_buckets, bucket_size, self.increase_collisions, self.increase_overflows)
        self._collisions = 0
        self._overflows = 0
        self._pages = tuple([Page(page_size) for _ in range(self._n_pages)])

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

    @property
    def bucket_size(self):
        return self._index.bucket_size

    @property
    def n_buckets(self):
        return self._index.n_buckets

    @property
    def page_size(self):
        return self._index.page_size

    @property
    def n_pages(self):
        return self._index.n_pages

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def set_pages(self, _):
        raise Exception("Pages cannot be set directly")

    def increase_collisions(self):
        self._collisions += 1

    def increase_overflows(self):
        self._overflows += 1

    def table_scan(self, item: str) -> int | None:
        time_a = time.monotonic_ns()
        for i, page in enumerate(self._pages):
            if item in page.items:
                time_b = time.monotonic_ns()
                return i, (time_b - time_a) / 1e6
        else:
            time_b = time.monotonic_ns()
            return -1, (time_b - time_a) / 1e6

    def fill(self, regs: list[str]):
        for reg in regs:
            for i, page in enumerate(self._pages):
                if not page.is_full():
                    page.add(reg)
                    self.index.add(reg, i)
                    break
            else:
                raise Exception("All pages are full")

    def query(self, item: str) -> int | None:
        return self.index.search(item)


if __name__ == "__main__":
    db = Database()
    db.fill(WORDS)
    print(f"Collisions: {db.collisions}")
    print(f"Overflows: {db.overflows}")

    print("\nQuerying for 'banana'...")
    page_address, query_time = db.query("banana")
    print(f"Page address: {page_address}, Query time: {query_time} ms")

    print("\nPerforming a table scan for 'banana'...")
    page_address, scan_time = db.table_scan("banana")
    print(f"Page address: {page_address}, Table scan time: {scan_time} ms")
