"""Defines the core structure for modular features."""

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from flask import Flask
from flask import Response
from flask import render_template
from flask import send_from_directory


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


class Route(Feature, ABC):
    """Abstract base class for all routes."""

    @property
    @abstractmethod
    def path(self) -> str:
        """Get the URL path for the route."""
        pass

    @property
    @abstractmethod
    def view_func(self) -> Callable[..., Union[str, Response]]:
        """Get the view function for the route."""
        pass


class DynamicRoute(Route):
    """A route with a user-defined view function."""

    def __init__(
        self, path: str, view_func: Callable[..., Union[str, Response]]
    ) -> None:
        """Initialize a DynamicRoute with a specified path and view function."""
        self._path = path
        self._view_func = view_func

    @property
    def path(self) -> str:
        """Get the URL path for the route."""
        return self._path

    @property
    def view_func(self) -> Callable[..., Union[str, Response]]:
        """Get the view function for the route."""
        return self._view_func

    def register(self, app: Flask) -> None:
        """Register the route with the Flask app."""
        app.add_url_rule(self.path, view_func=self.view_func)

    def __repr__(self) -> str:
        """Return a string representation of DynamicRoute."""
        return f"<DynamicRoute path={self.path} view_func={self.view_func.__name__}>"


class StaticRoute(DynamicRoute):
    """A route for serving static files from a directory."""

    def __init__(self, url_prefix: str, directory: Path) -> None:
        """Initialize a StaticRoute for serving static files."""
        self._directory = directory.resolve()
        static_path = f"{url_prefix.rstrip('/')}/<path:filename>"

        # define the view function inline
        def static_view_func(filename: str) -> Response:
            return send_from_directory(str(self._directory), filename)

        super().__init__(static_path, static_view_func)

    def __repr__(self) -> str:
        """Return a string representation of StaticRoute."""
        return f"<StaticRoute path={self.path} directory={self._directory}>"


class TemplateRoute(DynamicRoute):
    """A route that renders a template."""

    def __init__(
        self, path: str, template_name: str, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize the TemplateRoute with path, template, and context."""
        self._template_name = template_name
        self._context = context or {}

        # define the view function inline
        def render_template_func() -> str:
            """Render the template with the provided context."""
            return render_template(self._template_name, **self._context)

        super().__init__(path, render_template_func)

    def _summarize_context(self, max_items: int = 3) -> str:
        """Return a summarized string of context key-value pairs."""
        items = list(self._context.items())
        summary = ", ".join(f"{k}={v!r}" for k, v in items[:max_items])
        if len(items) > max_items:
            summary += ", ..."
        return summary

    def __repr__(self) -> str:
        """Return a string representation of TemplateRoute."""
        context_summary = self._summarize_context()
        return (
            f"<TemplateRoute path={self.path} "
            f"template={self._template_name} "
            f"context={{ {context_summary} }}>"
        )


class AutoRoute(Route):
    """Automatically determine route type based on the arguments provided."""

    def __init__(
        self,
        path: str,
        view_func: Optional[Callable[..., Union[str, Response]]] = None,
        directory: Optional[Path] = None,
        template_file: Optional[str] = None,
    ) -> None:
        """Validate arguments, select the route, and instantiate route object."""
        # call _select_route with all the arguments passed in the constructor
        route_class, route_kwargs = self._select_route(
            view_func, directory, template_file
        )

        # instantiate the selected route class and store it
        self._route_object = route_class(path, **route_kwargs)

    def _select_route(
        self,
        view_func: Optional[Callable[..., Union[str, Response]]] = None,
        directory: Optional[Path] = None,
        template_file: Optional[str] = None,
    ) -> Tuple[Type[Union[DynamicRoute, StaticRoute, TemplateRoute]], Dict[str, Any]]:
        """Validate the arguments and select the appropriate route class."""
        provided_args = sum(
            1 for arg in [view_func, directory, template_file] if arg is not None
        )

        if provided_args > 1:
            raise ValueError(
                "You can only provide one of "
                "`view_func`, `directory`, or `template_file` to AutoRoute. "
                "Please be explicit about which route type you want to create."
            )
        elif view_func:
            return DynamicRoute, {"view_func": view_func}
        elif directory:
            return StaticRoute, {"directory": directory}
        elif template_file:
            return TemplateRoute, {"template_file": template_file}
        else:
            raise ValueError(
                "AutoRoute must have at least one of "
                "`view_func`, `directory`, or `template_file` specified."
            )

    @property
    def path(self) -> str:
        """Get the URL path for the actual route object."""
        # delegate to the selected route's path property
        return self._route_object.path

    @property
    def view_func(self) -> Callable[..., Union[str, Response]]:
        """Get the view function for the actual route object."""
        # delegate to the selected route's view_func
        return self._route_object.view_func

    def register(self, app: Flask) -> None:
        """Use actual route object to register with the Flask app."""
        # register the route object
        self._route_object.register(app)

    def __repr__(self) -> str:
        """Return a string representation of AutoRoute."""
        return (
            f"<AutoRoute path={self.path} "
            f"type={self._route_object.__class__.__name__}>"
        )


class IndexRoute(AutoRoute):
    """Convenience for AutoRoute at '/'."""

    def __init__(
        self,
        view_func: Optional[Callable[..., Union[str, Response]]] = None,
        directory: Optional[Path] = None,
        template_file: Optional[str] = None,
    ) -> None:
        """Initialize a specialized AutoRoute for the root ('/') path."""
        super().__init__(
            "/", view_func=view_func, directory=directory, template_file=template_file
        )
