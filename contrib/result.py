from dataclasses import dataclass, asdict

from typing import List


@dataclass
class PaginateResult:
    page: int
    per_page: int
    total_page: int
    items: List

    def to_dict(self):
        return asdict(self)
