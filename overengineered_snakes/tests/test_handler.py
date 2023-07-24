from hypothesis import given

from overengineered_snakes.handler import Handler
from overengineered_snakes.tests.strategies.handler import handler_st


@given(handler_st)
def test_handler_random_color(handler: Handler) -> None:
    color = handler.random_color()
    assert color in handler.colors
