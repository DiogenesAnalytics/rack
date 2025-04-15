"""Configuration file for pytest."""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """For configuring pytest with custom markers."""
    config.addinivalue_line("markers", "debug: debugging tests.")
    config.addinivalue_line("markers", "fixture: fixture tests.")
    config.addinivalue_line("markers", "concrete: concrete class tests.")
    config.addinivalue_line("markers", "abc: custom ABC tests.")
