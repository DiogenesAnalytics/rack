"""Common utilities for rack."""

import importlib.util
import inspect
from typing import Iterator
from typing import Type

from rack.website import Website


def discover_websites() -> Iterator[Type[Website]]:
    """Only search inside the 'rack.website' module."""
    module = importlib.import_module("rack.website")
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, Website) and obj is not Website:
            yield obj
