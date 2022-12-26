from abc import ABC
from abc import abstractmethod

from overengineered_snakes.backend import Handler


class AbstractRenderer(ABC):
    @abstractmethod
    def render(self, handler: Handler) -> None:
        pass
