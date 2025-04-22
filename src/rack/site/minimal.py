"""Provides minimal implementations of the `Site` interface."""

from pathlib import Path
from typing import Optional
from typing import Tuple

from flask import Flask
from flask import render_template

from rack.feature.route import IndexRoute
from rack.feature.route import Route
from rack.site.base import Site


class BasicSite(Site):
    """A minimal concrete implementation of the Site ABC."""

    def __init__(self, app: Optional[Flask] = None) -> None:
        """Initialize the site and configure static/template paths."""
        # if no app is provided, create a new Flask app with the class name
        app = app or Flask(self.__class__.__name__)
        super().__init__(app)

        static_path, template_path = self.get_default_paths()
        self.configure(static_folder=static_path, template_folder=template_path)

    def get_default_paths(self) -> Tuple[Path, Path]:
        """Return the default static and template folder paths."""
        base_path = Path(__file__).parent
        static_path = base_path / "static" / "site" / "basic"
        template_path = base_path / "templates" / "site" / "basic"
        return static_path, template_path

    @property
    def index_route(self) -> Route:
        """Defining the basic index route."""
        return IndexRoute(view_func=self.home_view)

    def home_view(self) -> str:
        """Render the homepage."""
        return render_template("index.html")
