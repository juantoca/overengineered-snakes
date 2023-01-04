from hypothesis import assume
from hypothesis.strategies import booleans
from hypothesis.strategies import composite
from hypothesis.strategies import DrawFn
from hypothesis.strategies import floats
from hypothesis.strategies import integers
from hypothesis.strategies import lists
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import tuples

from overengineered_snakes.backend.behaviours.simple import IA


@composite
def ia_st(
    draw: DrawFn,
    random_weight: SearchStrategy[bool] = booleans(),
    crazy_behaviour: SearchStrategy[bool] = booleans(),
    max_jump: SearchStrategy[int] = integers(min_value=1),
) -> IA:
    list_length = draw(integers(min_value=1, max_value=100))
    variacion = lists(
        tuples(integers(), integers()),
        min_size=list_length,
        max_size=list_length,
    )
    weight = lists(
        floats(min_value=0.001, max_value=100.0),
        min_size=list_length,
        max_size=list_length,
    )
    var = draw(variacion)
    weight_list = draw(weight)
    assume(len(var) == len(weight_list))
    return IA(
        variacion=var,
        weight=weight_list,
        random_weight=draw(random_weight),
        crazy_behaviour=draw(crazy_behaviour),
        max_jump=draw(max_jump),
    )
