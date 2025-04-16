"""Tests for module rack.__main__."""

import pytest
from click.testing import CliRunner

from rack.__main__ import main


@pytest.mark.cli
def test_version_option() -> None:
    """Test the version option."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


@pytest.mark.cli
def test_list_builtins() -> None:
    """Test the 'list-builtins' command."""
    runner = CliRunner()
    result = runner.invoke(main, ["list-builtins"])

    assert result.exit_code == 0
    assert "Available built-in website implementations:" in result.output
    assert "BasicWebsite" in result.output


@pytest.mark.cli
def test_run_with_test_mode() -> None:
    """Test the 'run' command with the --test flag."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "run",
            "--test",
            "--builtin",
            "BasicWebsite",
            "--host",
            "127.0.0.1",
            "--port",
            "5000",
            "--debug",
        ],
    )

    assert result.exit_code == 0
    assert "⚡ Test mode: Skipping server startup" in result.output
    assert "🛠️ Diagnostic Info:" in result.output
    assert " - Built-in: BasicWebsite" in result.output
    assert " - Host: 127.0.0.1" in result.output
    assert " - Port: 5000" in result.output
    assert " - Debug: Enabled" in result.output


@pytest.mark.cli
def test_run_with_invalid_builtin() -> None:
    """Test the 'run' command with an invalid built-in to ensure it fails."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "run",
            "--builtin",
            "NonExistentWebsite",
            "--host",
            "127.0.0.1",
            "--port",
            "5000",
        ],
    )

    assert result.exit_code != 0
    assert "❌ Built-in implementation 'NonExistentWebsite' not found." in result.output


@pytest.mark.cli
def test_invalid_command() -> None:
    """Test an invalid command to ensure an error is raised."""
    runner = CliRunner()
    result = runner.invoke(main, ["nonexistent-command"])

    assert result.exit_code != 0
    assert "Error: No such command 'nonexistent-command'." in result.output


@pytest.mark.cli
def test_help_option() -> None:
    """Test the '--help' option to ensure the help message is displayed."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.output
