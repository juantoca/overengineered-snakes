from typing import Tuple

from overengineered_snakes.backend.behaviours.simple import IA
from overengineered_snakes.backend.mapa import Mapa
from overengineered_snakes.backend.tiles.body import Body
from overengineered_snakes.backend.tiles.tile import Tile


class Head(Tile):  # Head of the snake

    """
    Class that represents the head of the snake. It does all the magic stuff
    """

    def __init__(
        self,
        coords: Tuple[int, int],
        behaviour: IA,
        color: int = 0,
        character: str = "0",
        transitable: bool = True,
        limit: int = -1,
        body_char: str = "#",
    ):
        """
        Constructor for the head class
        :param coords: Initial coords
        :param color: Color of the snake
        :param character: Character to represent the head
        :param transitable: Is it overwritable?
        :param behaviour: IA for the snake
        :param limit: Length limit for the snake
        """
        super().__init__(
            coords,
            color=color,
            character=character,
            transitable=transitable,
        )
        self.behaviour = behaviour
        self.start_coordinates = self.coords
        self.limit = limit
        self.trigered = False
        self.length = 0
        self.body_char = body_char
        self.nextone = self.coords

    def run(self, handler) -> bool:  # type: ignore
        """
        Method to update the status of the snake
        :param handler: Game class to modify
        :return: True if the head has died
        """
        self.nextone = self.coords
        die = False
        election = self.behaviour.choose(
            handler,
            self.coords,
        )  # We choose where to move
        if election:
            # If there is a possible tile, we move to the selected one
            self.move(election, handler)  # type: ignore
        else:
            die = True  # If not, we kill it
            self.die(handler)
        if (
            self.length == self.limit and not self.trigered
        ):  # We add the snake to the cleaner in case it has reached the length limit
            handler.removing.append(self.start_coordinates)
            self.trigered = True
        self.length += 1
        # Returns if the head has died(so the cleaner can give it a proper burial)
        return die

    def move(self, coords: Tuple[int, int], mapa: Mapa) -> None:
        """
        Moves the head
        :param coords: Coords to move to
        :param mapa: Game class to modify
        :return: VOID
        """
        mapa.set_coords(
            self.coords,
            Body(
                self.coords,
                coords,
                color=self.color,
                character=self.body_char,
                transitable=False,
            ),
        )  # We create a body part on previous location
        self.coords = coords
        # Finally, we change the destination tile to ourselfs
        mapa.set_coords(coords, self)

    def die(self, mapa: Mapa) -> None:
        """
        Kills the snake
        :param mapa: Game class to modify
        :return: VOID
        """
        mapa.set_coords(
            self.coords,
            Body(
                self.coords,
                self.coords,
                color=self.color,
                character=self.body_char,
                transitable=False,
            ),
        )  # Changes the tile
