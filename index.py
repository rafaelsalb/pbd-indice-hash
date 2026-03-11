from pprint import pprint
import time

from bucket import Bucket
from config import BUCKET_COUNT, BUCKET_SIZE, PAGE_COUNT, PAGE_SIZE
from hash_function import prime_sum
from words import WORDS


class Index:
    def __init__(self, n_buckets: int, bucket_size: int, increase_collisions=None, increase_overflows=None):
        self._buckets = tuple([Bucket(bucket_size, increase_collisions, increase_overflows) for _ in range(n_buckets)])
        self._n_buckets = n_buckets
        self._bucket_size = bucket_size

    @property
    def buckets(self):
        return self._buckets

    @property
    def n_buckets(self):
        return self._n_buckets

    @property
    def bucket_size(self):
        return self._bucket_size

    def add(self, item: str, page_address: int):
        _hash = prime_sum(item, self.n_buckets)
        try:
            self._buckets[_hash].add(item, page_address)
        except Exception as e:
            print(f"Error adding item '{item}' to bucket {_hash}: {e}")
        return

    def search(self, item: str) -> int | None:
        time_a = time.monotonic_ns()
        _hash = prime_sum(item, self.n_buckets)
        bucket = self._buckets[_hash]
        page_address = bucket.search(item)  # vai retornar -1 se não encontrar
        time_b = time.monotonic_ns()
        return page_address, (time_b - time_a) / 1e6
