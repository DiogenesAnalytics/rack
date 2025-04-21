"""Tests for module rack.feature.route."""

import inspect
from pathlib import Path

import pytest
from flask import Flask

from rack.feature.route import AutoRoute
from rack.feature.route import DynamicRoute
from rack.feature.route import IndexRoute
from rack.feature.route import Route
from rack.feature.route import StaticRoute
from rack.feature.route import TemplateRoute


@pytest.mark.route
@pytest.mark.feature
def test_route_is_abstract() -> None:
    """Ensure Route cannot be instantiated directly."""
    assert inspect.isabstract(Route)


@pytest.mark.route
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


@pytest.mark.route
@pytest.mark.feature
def test_route_repr() -> None:
    """Test that the __repr__ of Route returns expected string."""

    def test_func() -> str:
        return "Test"

    route = DynamicRoute("/test", test_func)
    assert repr(route) == "<DynamicRoute path=/test view_func=test_func>"


@pytest.mark.route
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


@pytest.mark.route
@pytest.mark.feature
def test_index_route_repr() -> None:
    """Test __repr__ of IndexRoute."""

    def index_func() -> str:
        return "Index"

    route = IndexRoute(view_func=index_func)
    assert repr(route) == "<AutoRoute path=/ type=DynamicRoute>"


@pytest.mark.route
@pytest.mark.feature
def test_autoroute_dynamic() -> None:
    """Test AutoRoute selects DynamicRoute when view_func is provided."""

    def dynamic_view() -> str:
        return "Dynamic"

    route = AutoRoute(path="/dynamic", view_func=dynamic_view)
    assert isinstance(route._route_object, DynamicRoute)


@pytest.mark.route
@pytest.mark.feature
def test_autoroute_static() -> None:
    """Test AutoRoute selects StaticRoute when directory is provided."""
    route = AutoRoute(path="/static", directory=Path("/some/path"))
    assert isinstance(route._route_object, StaticRoute)


@pytest.mark.route
@pytest.mark.feature
def test_autoroute_template() -> None:
    """Test AutoRoute selects TemplateRoute when template_file is provided."""
    route = AutoRoute(path="/template", template_file="template.html")
    assert isinstance(route._route_object, TemplateRoute)


@pytest.mark.route
@pytest.mark.feature
def test_autoroute_invalid() -> None:
    """Test AutoRoute raises ValueError for invalid argument combinations."""
    with pytest.raises(ValueError):
        AutoRoute(
            path="/invalid", template_file="template.html", directory=Path("/some/path")
        )


@pytest.mark.route
@pytest.mark.feature
def test_autoroute_invalid_raises_valueerror() -> None:
    """Test that AutoRoute raises a ValueError when no valid constructor."""
    with pytest.raises(ValueError):
        AutoRoute(path="/invalid")


@pytest.mark.route
@pytest.mark.feature
def test_staticroute_serves_file(tmp_path: Path) -> None:
    """Test that StaticRoute properly serves a static file from directory."""
    # create dummy file
    file_path = tmp_path / "test.txt"
    file_path.write_text("Static content")

    app = Flask(__name__)
    route = StaticRoute(url_prefix="/assets/files", directory=tmp_path)
    route.register(app)

    client = app.test_client()
    response = client.get("/assets/files/test.txt")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Static content"


@pytest.mark.route
@pytest.mark.feature
def test_templateroute_renders_template(tmp_path: Path) -> None:
    """Test that TemplateRoute correctly renders a Jinja2 template."""
    # setup template
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "hello.html").write_text("<h1>Hello {{ name }}</h1>")

    app = Flask(__name__, template_folder=str(templates_dir))

    route = TemplateRoute(
        path="/hello", template_file="hello.html", context={"name": "Alice"}
    )
    route.register(app)

    client = app.test_client()
    response = client.get("/hello")
    assert response.status_code == 200
    assert "<h1>Hello Alice</h1>" in response.get_data(as_text=True)
