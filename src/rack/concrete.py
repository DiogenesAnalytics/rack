"""Provides concrete implementations of rack.abc."""

from pathlib import Path
from typing import Optional

from flask import Flask
from flask import render_template

from rack.abc import Website


class BasicWebsite(Website):
    """A minimal concrete implementation of the Website ABC."""

    def __init__(self, app: Optional[Flask] = None) -> None:
        """Initialize the website and configure static/template paths."""
        # call parent constructor
        super().__init__(app)

        # get parent dir of the current file
        base_path: Path = Path(__file__).parent
        static_path: Path = base_path / "static" / "website" / "basic"
        template_path: Path = base_path / "templates" / "website" / "basic"

        # configure the Flask app's static and template folders
        self.app.static_folder = str(static_path)
        self.app.template_folder = str(template_path)

    def register_routes(self) -> None:
        """Register a basic homepage route."""

        @self.app.route("/")
        def home() -> str:
            """Render the homepage."""
            return render_template("index.html")
