from abc import ABC, abstractmethod
from typing import Any

from starlette.applications import Starlette


class HttpApp(ABC):
    """A2A Server application interface."""

    @abstractmethod
    def build(self, **kwargs: Any) -> Starlette:
        pass
