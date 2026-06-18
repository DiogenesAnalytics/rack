"""Route subpackage for modular route features."""

from rack.feature.route.base import AutoRoute
from rack.feature.route.base import DynamicRoute
from rack.feature.route.base import IndexRoute
from rack.feature.route.base import Route
from rack.feature.route.base import StaticRoute
from rack.feature.route.base import TemplateRoute


__all__ = [
    "Route",
    "DynamicRoute",
    "StaticRoute",
    "TemplateRoute",
    "AutoRoute",
    "IndexRoute",
]
