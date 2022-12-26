
from abc import ABC, abstractmethod

from overengineered_snakes.backend import Handler


class AbstractRenderer(ABC):

    @abstractmethod
    def render(self, handler: Handler):
        pass
