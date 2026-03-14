import time

from config import BUCKET_SIZE, PAGE_SIZE, REG_COUNT
from index import Index
from page import Page
from query_result import QueryResult
from words import WORDS


class Database:
    def __init__(self, bucket_size: int = BUCKET_SIZE, page_size: int = PAGE_SIZE):
        assert not bucket_size is None and bucket_size > 0, "Bucket size must be a positive integer"
        assert not page_size is None and page_size > 0, "Page size must be a positive integer"
        self._bucket_size = bucket_size
        self._page_size = page_size
        self._n_buckets = None
        self._n_pages = None
        self._index = None
        self._collisions = 0
        self._overflows = 0
        self._pages = None
        self._index_build_time = 0

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
        return self._bucket_size

    @property
    def n_buckets(self):
        return self._n_buckets

    @property
    def page_size(self):
        return self._page_size

    @property
    def n_pages(self):
        return self._n_pages

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def set_pages(self, _):
        raise Exception("Pages cannot be set directly")

    @property
    def index_build_time(self):
        return self._index_build_time

    def increase_collisions(self):
        self._collisions += 1

    def increase_overflows(self):
        self._overflows += 1

    def table_scan(self, item: str) -> int | None:
        time_a = time.monotonic_ns()
        for i, page in enumerate(self._pages):
            j = page.items.index(item) if item in page.items else -1
            if j != -1:
                time_b = time.monotonic_ns()
                return (i, j), (time_b - time_a) / 1e6
        else:
            time_b = time.monotonic_ns()
            return (-1, -1), (time_b - time_a) / 1e6

    def fill(self, regs: list[str]):
        self._n_buckets = 1 + (len(regs) // self.bucket_size)
        self._n_pages = 1 + (len(regs) // self.page_size)
        self._pages = tuple([Page(self.page_size, i) for i in range(self._n_pages)])
        self._index = Index(self._n_buckets, self.bucket_size, self.increase_collisions, self.increase_overflows)
        # assert self.n_buckets <= len(regs) / self.bucket_size, "O número de buckets deve ser maior que o número de registros dividido pelo tamanho do bucket para evitar colisões excessivas"
        time_a = time.monotonic_ns()
        for reg in regs:
            for page in self._pages:
                if not page.is_full():
                    address = page.add(reg)
                    self.index.add(reg, address)
                    break
            else:
                raise Exception("All pages are full")
        time_b = time.monotonic_ns()
        self._index_build_time = (time_b - time_a) / 1e6

    def query(self, item: str) -> int | None:
        print(f"Querying for item '{item}' using index...")
        result = self.index.search(item)
        if not result.found:
            print(f"Item '{item}' not found in index.")
            return QueryResult(
                found=False,
                page_index=-1,
                record_index=-1,
                search_time_ms=result.search_time_ms,
                bucket_index=result.bucket_index,
                bucket_position=result.bucket_position
            )
        return result

    def table_scan_query(self, item: str) -> int | None:
        time_a = time.monotonic_ns()
        for i, page in enumerate(self._pages):
            for j in range(page.size):
                if page.items[j] == item:
                    time_b = time.monotonic_ns()
                    return QueryResult(
                        found=True,
                        page_index=i,
                        record_index=j,
                        search_time_ms=(time_b - time_a) / 1e6
                    )
        time_b = time.monotonic_ns()
        return QueryResult(
            found=False,
            page_index=-1,
            record_index=-1,
            search_time_ms=(time_b - time_a) / 1e6
        )


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
