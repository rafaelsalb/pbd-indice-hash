from dataclasses import dataclass


@dataclass
class QueryResult:
    page_index: int
    record_index: int
    search_time_ms: float | None = None
    found: bool | None = None
