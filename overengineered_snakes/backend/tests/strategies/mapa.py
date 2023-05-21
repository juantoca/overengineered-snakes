from typing import Tuple

from hypothesis.strategies import builds
from hypothesis.strategies import characters
from hypothesis.strategies import composite
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


@composite
def random_chars_mapa_st(draw, mapas=empty_mapa_st, chars=characters()):  # type: ignore
    mapa: Mapa = draw(mapas)
    for _, tile in mapa:
        tile.character = draw(chars)
    return mapa
