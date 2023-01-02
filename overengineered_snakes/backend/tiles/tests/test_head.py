from hypothesis import given

from overengineered_snakes.backend.mapa import Mapa
from overengineered_snakes.backend.tests.strategies.mapa import empty_mapa_st
from overengineered_snakes.backend.tiles.body import Body
from overengineered_snakes.backend.tiles.head import Head
from overengineered_snakes.backend.tiles.tests.strategies.head import head_st


@given(head_st, empty_mapa_st)
def test_head_die(head: Head, mapa: Mapa) -> None:
    mapa.set_coords(head.coords, head)
    head.die(mapa)
    assert type(mapa.get_coords(head.coords)) is Body
