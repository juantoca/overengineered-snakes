from hypothesis.strategies import builds
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import text

from overengineered_snakes.backend.tiles.tile import Tile


tile_st: SearchStrategy[Tile] = builds(
    Tile,
    character=text().filter(
        lambda char: len(char) == 1,
    ),
)
