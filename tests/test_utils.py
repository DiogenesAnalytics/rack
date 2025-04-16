"""Tests for module rack.utils."""

import pytest

from rack.utils import discover_websites
from rack.website import Website


@pytest.mark.utils
def test_discover_websites_from_local_path() -> None:
    """Ensure that discover_websites correctly finds subclasses."""
    # find matches
    websites = list(discover_websites())

    # get names
    class_names = {cls.__name__ for cls in websites}

    # check
    assert "BasicWebsite" in class_names
    assert all(issubclass(cls, Website) for cls in websites)
