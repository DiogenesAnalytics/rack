"""Configuration file for pytest."""

from pathlib import Path
from textwrap import dedent

import pytest
from flask import Flask


def pytest_configure(config: pytest.Config) -> None:
    """For configuring pytest with custom markers."""
    config.addinivalue_line("markers", "debug: debugging tests.")
    config.addinivalue_line("markers", "fixture: fixture tests.")
    config.addinivalue_line("markers", "cli: __main__ module tests.")
    config.addinivalue_line("markers", "utils: utils module tests.")
    config.addinivalue_line("markers", "feature: feature module tests.")
    config.addinivalue_line("markers", "site: site module tests.")
    config.addinivalue_line("markers", "route: feature.route module tests.")
    config.addinivalue_line("markers", "minimal: site.minimal module tests.")
    config.addinivalue_line("markers", "bundle: feature.route.bundle module tests.")


@pytest.fixture
def mock_rack_directory(tmp_path: Path) -> Path:
    """Creates a temporary mock 'rack' directory with Python files."""
    # Create a mock directory structure
    mock_dir = tmp_path / "rack"
    mock_dir.mkdir()

    # Create mock Python files
    mock_file_1 = mock_dir / "website_1.py"
    mock_file_1.write_text(
        dedent(
            """
        from rack.site.base import Site

        class MyWebsite(Site):
            pass
    """
        )
    )

    mock_file_2 = mock_dir / "website_2.py"
    mock_file_2.write_text(
        dedent(
            """
        from rack.site.base import Site

        class AnotherWebsite(Site):
            pass
    """
        )
    )

    return mock_dir


@pytest.fixture
def flask_app() -> Flask:
    """Return a fresh Flask application for feature registration tests."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app
