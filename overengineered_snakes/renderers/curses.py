import curses
from overengineered_snakes.backend import Handler


class CursesRenderer():

    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):  # Curses shit
            curses.init_pair(i + 1, i, -1)
    

    def render(self, handler: Handler):
        self.stdscr.clear()
        for y in range(0, len(handler.grid)-1):
            y = handler.grid[y]
            for x in y:
                self.stdscr.addstr(x.character, curses.color_pair(x.color))
            self.stdscr.addstr("\n")
        for x in handler.grid[-1]:
            self.stdscr.addstr(x.character, curses.color_pair(x.color))
        self.stdscr.refresh()
