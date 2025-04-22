"""Tests for module rack.site.base."""

import inspect

import pytest

from rack.site.base import Site


@pytest.mark.site
def test_site_is_abstract() -> None:
    """Site should be abstract."""
    assert inspect.isabstract(Site)
