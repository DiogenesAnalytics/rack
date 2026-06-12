"""Defines the core structure for composite features."""

from abc import abstractmethod
from typing import Sequence

from flask import Flask

from rack.feature.base import Feature


class BundleFeature(Feature):
    """A feature composed of one or more child features.

    A BundleFeature forms a recursive composition tree of Features.
    Each child feature may be either a leaf Feature (e.g. Route)
    or another BundleFeature.

    Registration is performed depth-first: registering a BundleFeature
    recursively registers all child features with the Flask application
    in declaration order.

    This enables complex application capabilities to be composed from
    smaller, reusable feature units.
    """

    @property
    @abstractmethod
    def features(self) -> Sequence[Feature]:
        """Return the child features contained by this bundle."""
        pass

    def register(self, app: Flask) -> None:
        """Register all child features with the Flask application."""
        for feature in self.features:
            if not isinstance(feature, Feature):
                raise TypeError(f"Invalid feature: {feature!r}")
            feature.register(app)

    def __repr__(self) -> str:
        """Return a string representation of the bundle feature."""
        return f"<{self.__class__.__name__} " f"features={len(self.features)}>"
