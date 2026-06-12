"""Tests for module rack.feature.bundle.base."""

from __future__ import annotations

from typing import Sequence

import pytest
from flask import Flask

from rack.feature.base import Feature
from rack.feature.bundle.base import BundleFeature


class RecordingFeature(Feature):
    """A feature that records registration order."""

    def __init__(self, log: list[str], name: str) -> None:
        """Initialize recording feature with shared log and identifier."""
        self._log: list[str] = log
        self._name: str = name

    def register(self, app: Flask) -> None:
        """Record when this feature is registered."""
        self._log.append(self._name)

    def __repr__(self) -> str:
        """Return debug representation."""
        return f"<RecordingFeature {self._name}>"


@pytest.mark.bundle
def test_bundle_registers_features_in_order(flask_app: Flask) -> None:
    """Ensure BundleFeature registers child features in declaration order."""
    log: list[str] = []

    f1 = RecordingFeature(log, "A")
    f2 = RecordingFeature(log, "B")
    f3 = RecordingFeature(log, "C")

    class Bundle(BundleFeature):
        """Test bundle for ordering behavior."""

        @property
        def features(self) -> Sequence[Feature]:
            """Return child features in fixed order."""
            return (f1, f2, f3)

    Bundle().register(app=flask_app)

    assert log == ["A", "B", "C"]


@pytest.mark.bundle
def test_bundle_is_recursive(flask_app: Flask) -> None:
    """Ensure BundleFeature composes recursively in depth-first order."""
    log: list[str] = []

    a = RecordingFeature(log, "A")
    b = RecordingFeature(log, "B")

    class Inner(BundleFeature):
        """Inner bundle."""

        @property
        def features(self) -> Sequence[Feature]:
            """Return inner features."""
            return (a,)

    class Outer(BundleFeature):
        """Outer bundle containing inner bundle."""

        @property
        def features(self) -> Sequence[Feature]:
            """Return nested feature structure."""
            return (Inner(), b)

    Outer().register(app=flask_app)

    assert log == ["A", "B"]


@pytest.mark.bundle
def test_bundle_rejects_invalid_feature(flask_app: Flask) -> None:
    """Ensure BundleFeature rejects non-Feature children."""

    class NotAFeature:
        """Invalid feature type."""

        def register(self, app: Flask) -> None:
            """No-op register method."""
            pass

    class BadBundle(BundleFeature):
        """Bundle containing invalid feature."""

        @property
        def features(self) -> Sequence[Feature]:
            """Return invalid feature list."""
            return (NotAFeature(),)  # type: ignore[return-value]

    with pytest.raises(TypeError):
        BadBundle().register(app=flask_app)


@pytest.mark.bundle
def test_empty_bundle_does_not_fail(flask_app: Flask) -> None:
    """Ensure empty BundleFeature registers safely."""

    class EmptyBundle(BundleFeature):
        """Bundle with no children."""

        @property
        def features(self) -> Sequence[Feature]:
            """Return empty feature set."""
            return ()

    EmptyBundle().register(app=flask_app)
