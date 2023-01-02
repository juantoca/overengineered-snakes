from typing import Tuple

from hypothesis import given
from hypothesis.strategies import data
from hypothesis.strategies import DataObject
from hypothesis.strategies import floats
from hypothesis.strategies import integers
from hypothesis.strategies import lists
from hypothesis.strategies import tuples

from overengineered_snakes.backend.behaviours.simple import IA
from overengineered_snakes.backend.behaviours.tests.strategies.simple import ia_st
from overengineered_snakes.backend.mapa import Mapa
from overengineered_snakes.backend.tests.strategies.mapa import coords_st
from overengineered_snakes.backend.tests.strategies.mapa import empty_mapa_st


@given(ia_st(), empty_mapa_st, coords_st)
def test_posible_moves_empty_mapa(ia: IA, mapa: Mapa, coords: Tuple[int, int]) -> None:
    choosed_coords: Tuple[int, int] = ia.choose(mapa, coords)  # type: ignore
    variation = (choosed_coords[0] - coords[0], choosed_coords[1] - coords[1])
    assert variation in ia.variacion


@given(data(), ia_st())
def test_weighted_choice(data: DataObject, ia: IA) -> None:
    list_length = data.draw(integers(min_value=2, max_value=10))
    options = lists(
        tuples(integers(), integers()),
        min_size=list_length,
        max_size=list_length,
    )
    weights = lists(
        floats(min_value=0.001, max_value=100000),
        min_size=list_length,
        max_size=list_length,
    )
    options_ex = data.draw(options)
    weights_ex = data.draw(weights)
    results = ia.weighted_choice(options_ex, weights_ex)

    assert results in options_ex
