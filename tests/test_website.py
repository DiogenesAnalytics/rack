"""Tests for module rack.website."""

import inspect
from typing import Any
from typing import Dict

import pytest
from flask import Flask
from pytest import MonkeyPatch

from rack.website import BasicWebsite
from rack.website import Website


@pytest.fixture
def mock_basic_website(monkeypatch: MonkeyPatch) -> BasicWebsite:
    """Provides a BasicWebsite instance with render_template mocked."""
    monkeypatch.setattr(
        "rack.website.render_template", lambda template: f"Rendered {template}"
    )
    return BasicWebsite()


@pytest.mark.website
def test_website_is_abstract() -> None:
    """Website should be abstract."""
    assert inspect.isabstract(Website)


@pytest.mark.website
def test_index_route_is_registered(mock_basic_website: BasicWebsite) -> None:
    """Check that the index route is registered correctly."""
    # test client
    client = mock_basic_website.app.test_client()
    response = client.get("/")

    # check
    assert response.status_code == 200
    assert "Rendered index.html" in response.get_data(as_text=True)


@pytest.mark.website
def test_repr_contains_expected_info(mock_basic_website: BasicWebsite) -> None:
    """Method __repr__ should include route info and folder paths."""
    # get __repr__ method return value
    repr_str = repr(mock_basic_website)

    # check
    assert "BasicWebsite" in repr_str
    assert "static=" in repr_str
    assert "template=" in repr_str
    assert "/" in repr_str


@pytest.mark.website
def test_index_route_property_returns_route(mock_basic_website: BasicWebsite) -> None:
    """BasicWebsite.index_route should return a Route instance."""
    # get index route set
    route = mock_basic_website.index_route

    # check
    assert hasattr(route, "path")
    assert hasattr(route, "view_func")
    assert route.path == "/"


@pytest.mark.website
def test_configure_updates_folders(mock_basic_website: BasicWebsite) -> None:
    """Test that configure sets static and template folders."""
    # update dirs
    mock_basic_website.configure(
        static_folder="static_test", template_folder="template_test"
    )

    # get actual dirs set
    static_folder = mock_basic_website.app.static_folder
    template_folder = mock_basic_website.app.template_folder

    # check
    assert static_folder is not None and static_folder.endswith("static_test")
    assert template_folder is not None and template_folder.endswith("template_test")


@pytest.mark.website
def test_register_features_does_not_duplicate_routes(
    mock_basic_website: BasicWebsite,
) -> None:
    """Ensure repeated registration of the same route does not duplicate it."""
    # count the number of rules before re-registering
    before = len(mock_basic_website.app.url_map._rules)

    # register the same route again
    mock_basic_website.register_features([mock_basic_website.index_route])

    # count again
    after = len(mock_basic_website.app.url_map._rules)

    # should only add one new rule if not already present
    assert after == before + 1


@pytest.mark.website
def test_run_invokes_flask_run(
    monkeypatch: MonkeyPatch, mock_basic_website: BasicWebsite
) -> None:
    """Ensure that the run() method on BasicWebsite invokes Flask's app.run()."""
    # capture if run is called
    called: Dict[str, Any] = {}

    def fake_run(self: Flask, **kwargs: Any) -> None:
        """Fake Flask.run method to verify invocation."""
        called["was_called"] = True
        called["kwargs"] = kwargs

    # patch Flask.run with the fake
    monkeypatch.setattr("flask.Flask.run", fake_run)

    # call run
    mock_basic_website.run(debug=True)

    # assertions
    assert called.get("was_called") is True
    assert called.get("kwargs", {}).get("debug") is True
