"""Tests for module rack.concrete."""

from typing import Callable
from typing import Dict
from typing import Generator
from typing import Tuple

import pytest
from flask import Flask
from flask import Response
from pytest import MonkeyPatch

from rack.concrete import BasicWebsite


@pytest.fixture
def fake_render_template() -> (
    Generator[Tuple[Callable[[str], str], Dict[str, str]], None, None]
):
    """Fixture to mock render_template and capture the calls."""
    # setup closure dict
    calls: Dict[str, str] = {}

    # setup closure function
    def _fake_render_template(name: str) -> str:
        """Mock render_template function."""
        calls["template_name"] = name
        return f"Mocked: {name}"

    yield _fake_render_template, calls


@pytest.fixture
def basic_website() -> BasicWebsite:
    """Fixture to create a BasicWebsite instance."""
    return BasicWebsite()


@pytest.mark.concrete
def test_basic_website_initialization(basic_website: BasicWebsite) -> None:
    """Test that BasicWebsite initializes correctly."""
    assert isinstance(basic_website.app, Flask)
    assert isinstance(basic_website.app.static_folder, str)
    assert isinstance(basic_website.app.template_folder, str)

    assert "static/website/basic" in basic_website.app.static_folder
    assert "templates/website/basic" in basic_website.app.template_folder


@pytest.mark.concrete
def test_basic_website_register_routes(
    basic_website: BasicWebsite,
    fake_render_template: Tuple[Callable[[str], str], Dict[str, str]],
    monkeypatch: MonkeyPatch,
) -> None:
    """Test that the register_routes method creates a homepage route."""
    # extract the mock and captured calls
    mock_render, calls = fake_render_template

    # mock render_template using monkeypatch
    monkeypatch.setattr("rack.concrete.render_template", mock_render)

    # setup routes on Flask app
    basic_website.register_routes()

    # check if the route exists and returns the mocked response
    with basic_website.app.test_client() as client:
        response: Response = client.get("/")
        assert response.status_code == 200
        assert response.get_data(as_text=True) == "Mocked: index.html"

    # check that the mocked render_template was called with the expected template
    assert calls["template_name"] == "index.html"
