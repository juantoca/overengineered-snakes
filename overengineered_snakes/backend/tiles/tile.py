from typing import Tuple


class Tile:  # Just tiles

    """
    Super-class that represents the basic information for an object of the grid
    """

    def __init__(
        self,
        coords: Tuple[int, int],
        color: int = 0,
        character: str = " ",
        transitable: bool = True,
    ):
        """
        Constructor for the tile object
        :param coords: Initial coords of the object (x, y)
        :param color: Color of the object
        :param character: Character which will represent the object
        :param transitable: Self-explanatory
        """
        self.coords = coords
        self.character = character
        self.color = color
        self.transitable = transitable
        self.nextone = coords
