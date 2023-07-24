import hypothesis.strategies as st

from overengineered_snakes.backend.tests.strategies.mapa import dim_strategy
from overengineered_snakes.handler import Handler

handler_st = st.builds(
    Handler,
    dim_strategy,
    dim_strategy,
    st.lists(st.integers(), min_size=1),
)
