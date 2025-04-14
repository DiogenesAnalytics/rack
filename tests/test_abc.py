"""Tests for module rack.abc."""

from pathlib import Path

import pytest
from flask import Flask

from rack.abc import Website


class MockWebsite(Website):
    """Concrete class for testing Website ABC."""

    def register_routes(self) -> None:
        """Mock implementation of register_routes."""
        pass


@pytest.fixture
def test_website() -> MockWebsite:
    """Fixture to create a Website instance."""
    return MockWebsite()


def test_website_initialization(test_website: MockWebsite) -> None:
    """Test that the website initializes a Flask app."""
    assert isinstance(test_website.app, Flask)


def test_website_configure(test_website: MockWebsite) -> None:
    """Test that the configure method sets static and template folders."""
    # configure dirs
    test_website.configure(static_folder="static_dir", template_folder="template_dir")

    # check
    assert isinstance(test_website.app.static_folder, str)
    assert isinstance(test_website.app.template_folder, str)
    assert Path(test_website.app.static_folder).name == "static_dir"
    assert Path(test_website.app.template_folder).name == "template_dir"


def test_website_repr(test_website: MockWebsite) -> None:
    """Test the __repr__ method."""
    # configure dirs
    test_website.configure(static_folder="static_dir", template_folder="template_dir")

    # get __repr__
    repr_str = repr(test_website)

    # check
    assert "static_dir" in repr_str
    assert "template_dir" in repr_str


def test_website_run(test_website: MockWebsite) -> None:
    """Test that the run method exists."""
    assert callable(test_website.run)
