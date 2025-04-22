"""Tests for module rack.utils."""

import types
from pathlib import Path

import pytest

from rack.site.base import Site
from rack.utils import discover_sites
from rack.utils import find_site_subclasses
from rack.utils import load_module_from_file
from rack.utils import resolve_root_path
from rack.utils import scan_python_files


@pytest.mark.utils
def test_resolve_root_path_valid() -> None:
    """Ensure it resolves a valid path correctly."""
    base_path = Path(__file__).parent
    resolved = resolve_root_path(base_path)
    assert resolved == base_path.resolve()


@pytest.mark.utils
def test_resolve_root_path_invalid() -> None:
    """Ensure it raises an error for an invalid path."""
    invalid_path = Path("/invalid/path")
    with pytest.raises(ValueError, match="does not exist"):
        resolve_root_path(invalid_path)


@pytest.mark.utils
def test_scan_python_files(mock_rack_directory: Path) -> None:
    """Test Python files found within a directory."""
    files = scan_python_files(mock_rack_directory)
    assert len(files) > 0
    assert all(f.suffix == ".py" for f in files)
    assert not any(f.name == "__init__.py" for f in files)


@pytest.mark.utils
def test_load_module_from_file_valid(mock_rack_directory: Path) -> None:
    """Tests valid Python file loaded as a module."""
    test_file = mock_rack_directory / "website_1.py"
    module = load_module_from_file(test_file)
    assert isinstance(module, types.ModuleType)


@pytest.mark.utils
def test_load_module_from_file_invalid(mock_rack_directory: Path) -> None:
    """Tests invalid Python file not loaded."""
    invalid_file = mock_rack_directory / "non_existent.py"
    with pytest.raises(FileNotFoundError):
        load_module_from_file(invalid_file)


@pytest.mark.utils
def test_find_site_subclasses() -> None:
    """Test Site subclass found in module."""
    module = types.ModuleType("mock_module")
    mock_class = type("MockWebsite", (Site,), {})
    setattr(module, "MockWebsite", mock_class)  # noqa: B010

    subclasses = list(find_site_subclasses(module))  # Wrap in list
    assert len(subclasses) == 1
    assert subclasses[0] == mock_class


@pytest.mark.utils
def test_find_site_subclasses_excludes_base_class() -> None:
    """Test ABC site should be excluded."""
    module = types.ModuleType("mock_module")
    setattr(module, "Site", Site)  # noqa: B010

    subclasses = list(find_site_subclasses(module))  # Wrap in list
    assert len(subclasses) == 0


@pytest.mark.utils
def test_discover_sites(mock_rack_directory: Path) -> None:
    """Test mock package Site subclasses discovered."""
    websites = list(discover_sites(mock_rack_directory))
    assert len(websites) == 2  # We created two site subclasses
    assert any(w.__name__ == "MyWebsite" for w in websites)
    assert any(w.__name__ == "AnotherWebsite" for w in websites)
