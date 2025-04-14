"""Defines core abstract base classes (ABCs) for the platform framework."""

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Union

from flask import Flask


class Website(ABC):
    """Abstract base class for all website implementations."""

    def __init__(self, app: Optional[Flask] = None):
        """Initialize the website. Accepts an optional Flask app."""
        self.app = app or Flask(__name__)

    def configure(
        self,
        static_folder: Optional[Union[str, Path]] = None,
        template_folder: Optional[Union[str, Path]] = None,
    ) -> None:
        """Configure static and template folder paths if provided."""
        if static_folder is not None:
            self.app.static_folder = str(static_folder)
        if template_folder is not None:
            self.app.template_folder = str(template_folder)

    @abstractmethod
    def register_routes(self) -> None:
        """Register all necessary routes for the website."""
        pass

    def run(self, **kwargs: Any) -> None:
        """Run the Flask app."""
        self.app.run(**kwargs)

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the Website."""
        return (
            f"<{self.__class__.__name__} "
            f"static={self.app.static_folder!r} "
            f"template={self.app.template_folder!r}>"
        )
