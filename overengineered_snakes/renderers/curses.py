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
        for y_i, y in enumerate(range(0, len(mapa.grid))):
            y_array = mapa.grid[y]
            for x_i, x in enumerate(y_array):
                self.stdscr.addch(y_i, x_i, x.character, curses.color_pair(x.color))
        self.stdscr.refresh()
