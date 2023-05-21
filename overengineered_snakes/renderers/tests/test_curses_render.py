from typing import Any
from unittest.mock import Mock
from unittest.mock import patch

from hypothesis import given

from overengineered_snakes.backend.mapa import Mapa
from overengineered_snakes.backend.tests.strategies.mapa import empty_mapa_st
from overengineered_snakes.backend.tiles.tile import Tile
from overengineered_snakes.renderers.curses import CursesRenderer


@given(empty_mapa_st)
def test_curses_renderer(mapa: Mapa) -> None:
    mapa2 = Mapa(mapa.alto, mapa.ancho)

    def side_effect(y_i: int, x_i: int, character: str, _: Any) -> None:
        mapa2.set_coords((x_i, y_i), Tile((x_i, y_i), character=character))

    with patch(
        "overengineered_snakes.renderers.curses.CursesRenderer.__init__",
        Mock(return_value=None),
    ), patch(
        "overengineered_snakes.renderers.curses.curses",
        Mock(),
    ):
        renderer: CursesRenderer = CursesRenderer()
        renderer.stdscr = Mock()
        renderer.stdscr.addch = Mock(side_effect=side_effect)
        renderer.stdscr.refresh = Mock()
        renderer.render(mapa)

        renderer.stdscr.refresh.assert_called_once()

    for v1, v2 in zip(mapa, mapa2):
        _, tile1 = v1
        _, tile2 = v2
        assert tile1.character == tile2.character
