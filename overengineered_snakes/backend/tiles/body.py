from typing import Tuple

from overengineered_snakes.backend.tiles.tile import Tile


class Body(Tile):  # Body of the snake

    """
    Class that represents a body tile of an snake
    """

    def __init__(
        self,
        coords: Tuple[int, int],
        nextone: Tuple[int, int],
        color: int = 0,
        character: str = "#",
        transitable: bool = True,
    ):
        super().__init__(coords, color, character, transitable)
        self.nextone = nextone
