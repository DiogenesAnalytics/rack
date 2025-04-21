"""Tests for module rack.feature.base."""

import inspect

import pytest

from rack.feature.base import Feature


@pytest.mark.feature
def test_feature_is_abstract() -> None:
    """Ensure Feature cannot be instantiated directly."""
    assert inspect.isabstract(Feature)
