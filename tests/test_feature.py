"""Tests for module rack.feature."""

import inspect

import pytest
from flask import Flask

from rack.feature import DynamicRoute
from rack.feature import Feature
from rack.feature import IndexRoute


@pytest.mark.feature
def test_route_registers_to_app() -> None:
    """Test that a Route correctly registers to a Flask app."""
    app = Flask(__name__)

    def hello() -> str:
        return "Hello"

    route = DynamicRoute("/hello", hello)
    route.register(app)

    client = app.test_client()
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Hello"


@pytest.mark.feature
def test_route_repr() -> None:
    """Test that the __repr__ of Route returns expected string."""

    def test_func() -> str:
        return "Test"

    route = DynamicRoute("/test", test_func)
    assert repr(route) == "<DynamicRoute path=/test view_func=test_func>"


@pytest.mark.feature
def test_index_route_registers_to_root() -> None:
    """Test that IndexRoute registers to '/' path."""
    app = Flask(__name__)

    def index() -> str:
        return "Index"

    route = IndexRoute(view_func=index)
    route.register(app)

    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Index"


@pytest.mark.feature
def test_index_route_repr() -> None:
    """Test __repr__ of IndexRoute."""

    def index_func() -> str:
        return "Index"

    route = IndexRoute(view_func=index_func)
    assert repr(route) == "<AutoRoute path=/ type=DynamicRoute>"


@pytest.mark.feature
def test_feature_is_abstract() -> None:
    """Ensure Feature cannot be instantiated directly."""
    assert inspect.isabstract(Feature)
