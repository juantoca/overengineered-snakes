from hypothesis.strategies import builds
from hypothesis.strategies import SearchStrategy

from overengineered_snakes.backend.behaviours.tests.strategies.simple import ia_st
from overengineered_snakes.backend.tiles.head import Head


head_st: SearchStrategy[Head] = builds(
    Head,
    behaviour=ia_st(),
    color=...,
    character=...,
    transitable=...,
    limit=...,
    body_char=...,
)
