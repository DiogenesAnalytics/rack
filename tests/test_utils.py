"""Tests for module rack.utils."""

import types
from pathlib import Path

import pytest

from rack.utils import discover_websites
from rack.utils import find_website_subclasses
from rack.utils import load_module_from_file
from rack.utils import resolve_root_path
from rack.utils import scan_python_files
from rack.website import Website


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
def test_find_website_subclasses() -> None:
    """Test Website subclass found in module."""
    module = types.ModuleType("mock_module")
    mock_class = type("MockWebsite", (Website,), {})
    setattr(module, "MockWebsite", mock_class)  # noqa: B010

    subclasses = list(find_website_subclasses(module))  # Wrap in list
    assert len(subclasses) == 1
    assert subclasses[0] == mock_class


@pytest.mark.utils
def test_find_website_subclasses_excludes_base_class() -> None:
    """Test ABC Website should be excluded."""
    module = types.ModuleType("mock_module")
    setattr(module, "Website", Website)  # noqa: B010

    subclasses = list(find_website_subclasses(module))  # Wrap in list
    assert len(subclasses) == 0


@pytest.mark.utils
def test_discover_websites(mock_rack_directory: Path) -> None:
    """Test mock package Website subclasses discovered."""
    websites = list(discover_websites(mock_rack_directory))
    assert len(websites) == 2  # We created two website subclasses
    assert any(w.__name__ == "MyWebsite" for w in websites)
    assert any(w.__name__ == "AnotherWebsite" for w in websites)
