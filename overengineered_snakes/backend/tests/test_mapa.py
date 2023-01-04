from typing import Tuple

from hypothesis import given

from overengineered_snakes.backend.mapa import Mapa
from overengineered_snakes.backend.tests.strategies.mapa import coords_st
from overengineered_snakes.backend.tests.strategies.mapa import empty_mapa_st
from overengineered_snakes.backend.tiles.tests.strategies.tile import tile_st
from overengineered_snakes.backend.tiles.tile import Tile


@given(empty_mapa_st, tile_st, coords_st)
def test_mapa_setter(
    mapa: Mapa,
    tile: Tile,
    coords: Tuple[int, int],
) -> None:
    mapa.set_coords(coords, tile)
    assert mapa.get_coords(coords) is tile


@given(empty_mapa_st, coords_st)
def test_mapa_coord_wrapping(mapa: Mapa, coords: Tuple[int, int]) -> None:
    normalized_coords = (coords[0] % mapa.ancho, coords[1] % mapa.alto)
    assert mapa.get_coords(normalized_coords) is mapa.get_coords(coords)


@given(empty_mapa_st)
def test_mapa_default(mapa: Mapa) -> None:
    possible_coords = [(x, y) for x in range(mapa.ancho) for y in range(mapa.alto)]
    assert all([type(mapa.get_coords(coords)) is Tile for coords in possible_coords])
