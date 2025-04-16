"""Defines the core structure for modular features."""

from abc import ABC
from abc import abstractmethod
from typing import Callable

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


class Route(Feature):
    """A feature representing a route."""

    def __init__(self, path: str, view_func: Callable[..., str]) -> None:
        """Initialize a Route feature."""
        self.path = path
        self.view_func = view_func

    def register(self, app: Flask) -> None:
        """Register the route with the Flask app."""
        app.add_url_rule(self.path, view_func=self.view_func)

    def __repr__(self) -> str:
        """Return a string representation of the Route feature."""
        return f"<Route path={self.path} view_func={self.view_func.__name__}>"


class IndexRoute(Route):
    """An index route that defaults to '/'."""

    def __init__(self, view_func: Callable[..., str]) -> None:
        """Initialize the IndexRoute, defaults to '/'."""
        super().__init__("/", view_func)
