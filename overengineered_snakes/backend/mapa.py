from typing import Tuple

from overengineered_snakes.backend.tiles.tile import Tile


class Mapa:
    def __init__(self, alto: int, ancho: int):
        """
        Constructor class for the map
        :param alto: height
        :param ancho: width
        """
        self.alto = alto
        self.ancho = ancho
        self.grid = self.gen_grid()

    def gen_grid(self) -> list[list[Tile]]:
        """
        Generates the grid matrix, filing it with empty tiles
        :return: Matrix map
        """
        returneo: list[list[Tile]] = []
        for y in range(0, self.alto):
            returneo.append([])
            for x in range(0, self.ancho):
                returneo[y].append(Tile((x, y)))
        return returneo

    def get_coords(self, coords: Tuple[int, int]) -> Tile:
        """
        Return the object at given coords
        :param coords: Coordinates to search in
        :return: (x, y) or False if not a valid tile
        """
        return self.grid[coords[1] % len(self.grid)][coords[0] % len(self.grid[0])]

    def set_coords(self, coords: Tuple[int, int], objeto: Tile) -> bool | None:
        """
        Changes the object at given coords
        :param coords: Coordinates to change
        :param objeto: Object to insert
        :return: False if not a valid position
        """
        try:
            self.grid[coords[1] % len(self.grid)][
                coords[0] % len(self.grid[0])
            ] = objeto
            return None
        except IndexError:
            return False
