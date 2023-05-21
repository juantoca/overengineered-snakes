import random
from typing import Any
from typing import Tuple

from overengineered_snakes.backend.behaviours.simple import IA
from overengineered_snakes.backend.mapa import Mapa
from overengineered_snakes.backend.tiles.head import Head
from overengineered_snakes.backend.tiles.tile import Tile


class Handler(Mapa):
    def __init__(
        self,
        alto: int,
        ancho: int,
        colors: list[int],
        percentage: float = 25,
        clean: bool = True,
        headlimit: int = 1,
        max_length: int = -1,
        random_weight: bool = True,
        crazy_behaviour: bool = False,
        max_jump: int = 5,
        body_char: str = "#",
        head_char: str = "O",
    ):
        """
        Constructor class for Handler
        :param alto: Height
        :param ancho: Width
        :param colors: List of available colors
        :param percentage: Probability of creating a new snake
        :param clean: Shall I clean the corpses?
        :param headlimit: Maximum snakes, infinite if negative
        :param max_length: Max length of snakes, infinite if negative
        :param random_weight: Shall I random-weight the snakes?
        :param crazy_behaviour: Shall I create
        random-behavioured snakes?
        :param max_jump: If crazy_behaviour,
        Which should be the maximum variation for both axes?
        """
        super().__init__(alto, ancho)
        self.percentage = percentage
        self.clear = clean
        self.limit_length = max_length
        self.random_weight = random_weight
        self.crazy_behaviour = crazy_behaviour
        self.max_jump = max_jump
        self.colors = colors
        self.grid = self.gen_grid()
        self.heads: list[Head] = []
        self.removing: list[Tuple[int, int]] = []
        self.head_limit = headlimit
        self.max_length = 0
        self.body_char = body_char
        self.head_char = head_char

    def run(self, gen: bool = True) -> dict[str, Any]:
        """
        Runs a turn
        :param gen: Shall I generate new snakes?
        :return: Status dictionary
        """
        filled = False
        delete: list[Head] = []
        for x in range(0, len(self.heads)):  # Updates the heads
            die = self.heads[x].run(self)
            if die:
                if self.heads[x].start_coordinates not in self.removing:
                    self.removing.append(self.heads[x].start_coordinates)
                    # We set that there's a new snake that needs a meatgrinder session
                delete.append(self.heads[x])
            if (
                self.heads[x].at_maximum_length
                and self.heads[x].start_coordinates not in self.removing
            ):
                self.removing.append(self.heads[x].start_coordinates)
        for x_ in delete:
            self.heads.remove(x_)
        if self.clear:
            self.clean()  # Do some magic, just don't touch it
        if gen:
            filled = self.gen_head()  # Gen the heads
        return self.status(filled)

    def status(self, filled: bool) -> dict[str, Any]:
        """
        Generates the status dictionary
        :return: {"snakes", "average length", "removing", "max_length"}
        """
        heads = self.heads
        sum_length = 0
        for x in heads:
            sum_length += x.length
            if x.length > self.max_length:
                self.max_length = x.length
        try:
            average = sum_length / len(heads)
        except ZeroDivisionError:
            average = 0
        returneo = {
            "snakes": len(self.heads),
            "average length": average,
            "removing": len(self.removing),
            "max_length": self.max_length,
            "filled": filled,
        }
        return returneo

    def clean(self) -> None:  # Harry Potter would be proud of this method
        """
        Cleans the game from corpses
        :return: VOID
        """
        remove = []  # We store the coords of the snakes that has been deleted completly
        for x in range(0, len(self.removing)):
            coords = self.removing[x]
            tile = self.get_coords(coords)
            nexts = tile.nextone  # We store the next position of the snake
            self.removing[x] = nexts
            if nexts == coords:
                # This means that it was the last
                # position so we delete it from erasing list
                remove.append(coords)
            self.set_coords(coords, Tile(coords))  # Finally, we clean the tile
        for x_ in remove:
            # And now, he would hit me 'cause a magician never show its tricks
            self.removing.remove(x_)

    def gen_head(self) -> bool:
        """
        Generates a new head
        :return: VOID
        """
        filled = False
        percentage = self.percentage
        while percentage > 0 and not filled:
            percentage -= 100
            if (
                random.randint(0, 100) <= self.percentage
                and len(self.heads) != self.head_limit
                and not filled
            ):
                salir = 100000
                while salir > 0:
                    coords = (
                        random.randint(0, self.ancho - 1),
                        random.randint(0, self.alto - 1),
                    )
                    if self.get_coords(coords).transitable:
                        ia = IA(
                            random_weight=self.random_weight,
                            crazy_behaviour=self.crazy_behaviour,
                            max_jump=self.max_jump,
                        )
                        head = Head(
                            coords,
                            character=self.head_char,
                            color=self.random_color(),
                            transitable=False,
                            behaviour=ia,
                            limit=self.limit_length,
                            body_char=self.body_char,
                        )
                        self.heads.append(head)
                        self.set_coords(coords, head)
                        salir = 0
                    else:
                        salir -= 1
                        if salir < 1:
                            filled = True
            else:
                percentage = -1
        return filled

    def random_color(self) -> int:
        """
        Returns a random color index
        :return: Random color index
        """
        return random.choice(self.colors)
