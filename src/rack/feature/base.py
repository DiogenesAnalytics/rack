"""Defines the core structure for modular features."""

from abc import ABC
from abc import abstractmethod

from flask import Flask


class Feature(ABC):
    """Abstract base class for modular features."""

    @abstractmethod
    def register(self, app: Flask) -> None:
        """Register routes, blueprints, context processors, etc."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation of the feature."""
        pass
