
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:

    clear: bool
    percentage: float
    fps: int
    max_length: int
    limit: int
    random_weighted: bool
    crazy: bool
    justCalculating: bool
    cicles: int
    seed: Optional[int]
    filled: bool
    timeout: int
    head: str
    body: str