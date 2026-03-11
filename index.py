import time

from bucket import Bucket
from hash_function import prime_sum
from index_result import IndexResult
from query_result import QueryResult


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

    def add(self, item: str, page_address: tuple[int, int]):
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
        print(f"Searching for item '{item}' in bucket {_hash}")
        bucket_position, (page_index, record_index) = bucket.search(item)  # vai retornar -1 se não encontrar
        time_b = time.monotonic_ns()
        result = IndexResult(
            found=page_index != -1,
            search_time_ms=(time_b - time_a) / 1e6,
            bucket_index=_hash,
            bucket_position=bucket_position if page_index != -1 else None,
            query_result=QueryResult(page_index=page_index, record_index=record_index)
        )
        return result
