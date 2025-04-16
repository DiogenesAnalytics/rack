"""Configuration file for pytest."""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """For configuring pytest with custom markers."""
    config.addinivalue_line("markers", "debug: debugging tests.")
    config.addinivalue_line("markers", "fixture: fixture tests.")
    config.addinivalue_line("markers", "cli: __main__ module tests.")
    config.addinivalue_line("markers", "utils: utils module tests.")
    config.addinivalue_line("markers", "feature: feature module tests.")
    config.addinivalue_line("markers", "website: website module tests.")
