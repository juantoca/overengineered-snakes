from dataclasses import dataclass


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
    seed: int | None
    filled: bool
    timeout: int
    head: str
    body: str
