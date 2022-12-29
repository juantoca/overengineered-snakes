import random
from typing import Tuple

from overengineered_snakes.backend.mapa import Mapa


class IA:  # Seems like our snakes are becoming intelligent
    def __init__(
        self,
        variacion: list[Tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)],
        weight: list[int] = [1, 1, 1, 1],
        random_weight: bool = True,
        crazy_behaviour: bool = False,
        max_jump: int = 10,
    ):
        """
        IA for the snakes
        :param variacion: Tuple of possible variations of the current position
        :param weight: Probability weights of the variations
        :param random_weight: Shall I generate random weights?
        :param crazy_behaviour: Shall I generate random variations?
        :param max_jump: If crazy_behaviour,
        Which is the maximum variation in both axes?
        """
        self.variacion = variacion
        self.weight = weight
        if random_weight:
            self.random_weight()
        if crazy_behaviour:
            self.crazy_behaviour(jump_limit=max_jump)

    def posible_moves(
        self,
        mapa: Mapa,
        coords: Tuple[int, int],
    ) -> Tuple[list[Tuple[int, int]], list[float]]:
        """
        Checks which of the variation-appointed tiles are available to move to
        :param mapa: Game class to check in
        :param coords: Current coords
        :return: Tuple of tuples = (possibilities, weights)
        """
        possibilities = []  # Coordinates
        weight: list[float] = []  # Weights
        longitud = len(self.variacion)
        for x in range(0, longitud):
            coordinates = (
                self.variacion[x][0] + coords[0],
                self.variacion[x][1] + coords[1],
            )
            tile = mapa.get_coords(coordinates)
            if tile and tile.transitable:  # We check if the tile is free
                possibilities.append(coordinates)
                weight.append(self.weight[x])
        return possibilities, weight

    def choose(self, mapa: Mapa, coords: Tuple[int, int]) -> Tuple[int, int] | bool:
        """
        Chooses where the snake should move
        :param mapa: Game class to use
        :param coords: Current coordinates
        :return: Coordinates or False if not valid destination
        """
        possibilities = self.posible_moves(mapa, coords)
        possibilities = self.modify_weights(
            possibilities[0],
            possibilities[1],
            mapa,
        )
        option: bool | Tuple[int, int] = False
        # If there is a possible tile, we choose a random-weighted possible position
        if len(possibilities[0]) > 0:
            option = self.weighted_choice(possibilities[0], possibilities[1])
        return option

    def modify_weights(
        self,
        possibilities: list[Tuple[int, int]],
        weight: list[float],
        mapa: Mapa,
    ) -> Tuple[list[Tuple[int, int]], list[float]]:
        """
        Checks the enviroment and modify the weights to make the best choice
        :param possibilities: Posible options
        :param weight: Weights of the options
        :param mapa: Game class
        :return: (possibilities, weights)
        """
        weighted: list[float] = []
        for x in range(0, len(possibilities)):
            coords = possibilities[x]
            adjacents = 0
            for (
                y
            ) in (
                self.variacion
            ):  # We count the number of bodys around a given possibility
                coordinates = (y[0] + coords[0], y[1] + coords[1])
                tile = mapa.get_coords(coordinates)
                if not tile or (tile and tile.__class__.__name__ == "Body"):
                    adjacents += 1
            if (
                adjacents == 0
            ):  # In case of no adjacency, we give privileges to the option
                weighted.append(weight[x] * 100)
            elif (
                adjacents == 3
            ):  # If it would die in the next cicle, we set the minimum weight
                weighted.append(0.001)
            else:  # If not, we give less priority based on the number of adjacent tiles
                weighted.append(weight[x] / adjacents)
        return possibilities, weighted

    def weighted_choice(  # type: ignore
        self,
        options: list[tuple[int, int]],
        weight: list[float],
    ) -> tuple[int, int]:
        """
        Makes a choice based on the weights
        :param options: Possibilities to choose from
        :param weight: Weights of the possibilities
        :return: options element choosen
        """
        chooser = []
        counter = 0.0
        for x in weight:
            counter += x
            chooser.append(counter)
        # We generate a random number between 0 and the sum of the weights
        eleccion = random.uniform(0, chooser[-1])
        for x in range(0, len(chooser)):
            if eleccion < chooser[x]:
                return options[x]

    def random_weight(self) -> None:
        """
        Generates random weights
        :return: VOID
        """
        total_weight = 0.0
        maximum_weigth = 1
        for x in range(0, len(self.weight)):
            weight = random.uniform(0.001, maximum_weigth)
            total_weight += weight
            self.weight[x] = weight  # type: ignore

    def crazy_behaviour(self, jump_limit: int = 2) -> None:
        """
        Generates random variations
        :param jump_limit: Limit of variation on both axes
        :return: VOID
        """
        for x in range(0, len(self.variacion)):
            self.variacion[x] = (
                random.randint(
                    -jump_limit,
                    jump_limit,
                ),
                random.randint(-jump_limit, jump_limit),
            )
