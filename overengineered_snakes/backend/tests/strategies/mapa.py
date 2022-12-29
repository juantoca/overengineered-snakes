from typing import Tuple

from hypothesis.strategies import builds
from hypothesis.strategies import integers
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import tuples

from overengineered_snakes.backend.mapa import Mapa


_dim_strategy: SearchStrategy[int] = integers(min_value=1, max_value=100)
empty_mapa_st: SearchStrategy[Mapa] = builds(
    Mapa,
    alto=_dim_strategy,
    ancho=_dim_strategy,
)

coords_st: SearchStrategy[Tuple[int, int]] = tuples(integers(), integers())
