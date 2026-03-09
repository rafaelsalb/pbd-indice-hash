from pprint import pprint
import time

from bucket import Bucket
from config import BUCKET_COUNT, BUCKET_SIZE, PAGE_COUNT, PAGE_SIZE
from hash_function import prime_sum
from page import Page
from words import WORDS


class Index:
    def __init__(self, n_buckets: int, bucket_size: int, n_pages: int, page_size: int, increase_collisions=None, increase_overflows=None):
        self._buckets = tuple([Bucket(bucket_size, increase_collisions, increase_overflows) for _ in range(n_buckets)])
        self._pages = tuple([Page(page_size) for _ in range(n_pages)])
        self._n_buckets = n_buckets
        self._bucket_size = bucket_size
        self._n_pages = n_pages
        self._page_size = page_size

    @property
    def buckets(self):
        return self._buckets

    @property
    def pages(self):
        return self._pages

    @property
    def n_buckets(self):
        return self._n_buckets

    @property
    def bucket_size(self):
        return self._bucket_size

    @property
    def n_pages(self):
        return self._n_pages

    @property
    def page_size(self):
        return self._page_size

    def add(self, item: str):
        for page in self._pages:
            if not page.is_full():
                page.add(item)
                _hash = prime_sum(item, self.n_buckets)
                self._buckets[_hash].add(item)
                return
        else:
            raise Exception("All pages are full")

    def search(self, item: str) -> int | None:
        time_a = time.monotonic_ns()
        _hash = prime_sum(item, self.n_buckets)
        bucket = self._buckets[_hash]
        found = item in bucket.items
        time_b = time.monotonic_ns()
        return found, (time_b - time_a) / 1e6

    def fill(self, regs: list[str]):
        for reg in regs:
            self.add(reg)


if __name__ == "__main__":
    dictionary = WORDS
    n = len(dictionary)
    index = Index(n_buckets=BUCKET_COUNT, bucket_size=BUCKET_SIZE, n_pages=PAGE_COUNT, page_size=PAGE_SIZE)
    index.fill(dictionary)

    test_words = ["a", "aboundingly", "hash", "index", "nonexistentword", "python", "the"]
    # print(test_words)

    # Test search
    for word in test_words:
        found, time_taken = index.search(word)
        if found:
            print(f"Search for '{word}': {time_taken} milliseconds")
        else:
            print(f"'{word}' not found in index. Search took {time_taken} milliseconds")

    print()

    # Search without index (table scan)
    items = []
    for page in index.pages:
        items.extend(page._items)
    # pprint(items)
    for word in test_words:
        time_a = time.monotonic_ns()
        found = word in items
        time_b = time.monotonic_ns()
        print(f"Table scan for '{word}': {(time_b - time_a) / 1e6} milliseconds. Found: {found}")
