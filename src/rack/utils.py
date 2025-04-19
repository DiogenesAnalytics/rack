"""Common utilities for rack."""

import importlib.util
import inspect
import sys
import types
from pathlib import Path
from typing import Iterator
from typing import List
from typing import Type
from typing import Union

from rack.website import Website


def resolve_root_path(base: Union[str, Path]) -> Path:
    """Resolve the root path to scan for Python modules."""
    path = Path(base).resolve()
    if not path.exists():
        raise ValueError(f"Path {path} does not exist.")
    return path


def scan_python_files(root: Path) -> List[Path]:
    """Recursively scan the root path for Python files."""
    return [p for p in root.rglob("*.py") if p.name != "__init__.py"]


def load_module_from_file(file_path: Path) -> types.ModuleType:
    """Load a module dynamically from a Python file path."""
    module_name = file_path.stem + "_" + str(abs(hash(file_path)))
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"Could not load module from {file_path}")


def find_website_subclasses(mod: types.ModuleType) -> Iterator[Type[Website]]:
    """Find all subclasses of Website in the given module."""
    for _, obj in inspect.getmembers(mod, inspect.isclass):
        bases = [base.__name__ for base in getattr(obj, "__bases__", [])]
        if "Website" in bases and obj.__name__ != "Website":
            yield obj


def discover_websites(base_path: Union[str, Path]) -> Iterator[Type[Website]]:
    """Discover all subclasses of `Website`."""
    root = resolve_root_path(base_path)
    for file in scan_python_files(root):
        mod = load_module_from_file(file)
        yield from find_website_subclasses(mod)
