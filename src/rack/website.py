"""Defines the core structure for website implementations."""

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Union

from flask import Flask
from flask import render_template

from rack.feature import Feature
from rack.feature import IndexRoute
from rack.feature import Route


class Website(ABC):
    """Abstract base class for all website implementations."""

    def __init__(self, app: Optional[Flask] = None):
        """Initialize the website. Accepts an optional Flask app."""
        # setup flask
        self.app = app or Flask(__name__)

        # register features
        self.register_features([self.index_route])

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

    def register_features(self, features: Iterable[Feature]) -> None:
        """Register each feature with the Flask app."""
        for feature in features:
            feature.register(self.app)

    @property
    @abstractmethod
    def index_route(self) -> Route:
        """Subclasses must implement an index route."""
        pass

    def run(self, **kwargs: Any) -> None:
        """Run the Flask app."""
        self.app.run(**kwargs)

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the Website."""
        # get list of routes from app.url_map
        routes = [
            f"{rule.endpoint!r} -> {rule}" for rule in self.app.url_map.iter_rules()
        ]
        routes_str = "\n    ".join(routes) if routes else "No routes registered"

        # build and return the final representation string
        return (
            f"<{self.__class__.__name__} "
            f"static={self.app.static_folder!r} "
            f"template={self.app.template_folder!r} "
            f"routes:\n    {routes_str}>"
        )


class BasicWebsite(Website):
    """A minimal concrete implementation of the Website ABC."""

    def __init__(self, app: Optional[Flask] = None) -> None:
        """Initialize the website and configure static/template paths."""
        super().__init__(app)

        static_path, template_path = self.get_default_paths()
        self.configure(static_folder=static_path, template_folder=template_path)

    def get_default_paths(self) -> Tuple[Path, Path]:
        """Return the default static and template folder paths."""
        base_path = Path(__file__).parent
        static_path = base_path / "static" / "website" / "basic"
        template_path = base_path / "templates" / "website" / "basic"
        return static_path, template_path

    @property
    def index_route(self) -> Route:
        """Defining the basic index route."""
        return IndexRoute(view_func=self.home_view)

    def home_view(self) -> str:
        """Render the homepage."""
        return render_template("index.html")
