import curses

from overengineered_snakes.backend.mapa import Mapa


class CursesRenderer:
    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):  # Curses shit
            curses.init_pair(i + 1, i, -1)

    def render(self, mapa: Mapa) -> None:
        for coords, tile in mapa:
            x_i, y_i = coords
            self.stdscr.addch(y_i, x_i, tile.character, curses.color_pair(tile.color))
        self.stdscr.refresh()
