from dataclasses import dataclass

from query_result import QueryResult


@dataclass
class IndexResult:
    found: bool
    search_time_ms: float
    bucket_index: int
    bucket_position: int
    query_result: QueryResult
