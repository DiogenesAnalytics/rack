"""Command-line interface for rack."""

from pathlib import Path
from typing import Any
from typing import Callable

import click

import rack
from rack.utils import discover_websites


DEFAULT_RACK_PATH = Path(rack.__file__).parent


def get_base_path(path: str) -> Path:
    """Helper function to determine the base path for discovering websites."""
    return Path(path).resolve()


def path_option(func: Callable[..., Any]) -> Callable[..., Any]:
    """A decorator that adds the '--path' option to a CLI command."""
    return click.option(
        "--path",
        default=DEFAULT_RACK_PATH,
        show_default=True,
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
        help="Path to the directory to scan for website implementations.",
    )(func)


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
def main() -> None:
    """Command-line interface for the Rack package."""


@main.command("list-builtins")
@path_option
def list_builtins(path: Path) -> None:
    """Lists all built-in Website implementations."""
    click.echo("Available built-in website implementations:")

    # Use the helper function to resolve the base path
    base_path = get_base_path(str(path))
    for cls in discover_websites(base_path):
        click.echo(f" - {cls.__name__}")


@main.command("run")
@click.option(
    "--builtin",
    type=str,
    help="Name of the built-in Website implementation to run (e.g., BasicWebsite).",
)
@click.option("--host", default="127.0.0.1", help="Host to run on.")
@click.option("--port", default=5000, help="Port to run on.")
@click.option("--debug", is_flag=True, help="Enable debug mode.")
@click.option("--test", is_flag=True, help="Run in test mode.")
@path_option
def run(
    builtin: str, host: str, port: int, debug: bool, test: bool, path: Path
) -> None:
    """Run a Website implementation — either built-in or from app.py/main.py."""
    # check for test option
    if test:
        click.echo("⚡ Test mode: Skipping server startup")
        click.echo("🛠️ Diagnostic Info:")
        click.echo(f" - Built-in: {builtin if builtin else None}")
        click.echo(f" - Host: {host}")
        click.echo(f" - Port: {port}")
        click.echo(f" - Debug: {'Enabled' if debug else 'Disabled'}")

    # check for builtin option
    elif builtin:
        base_path = get_base_path(str(path))
        implementations = {cls.__name__: cls for cls in discover_websites(base_path)}

        if builtin not in implementations:
            click.echo(f"❌ Built-in implementation {builtin!r} not found.\n")
            click.echo("✅ Available options:")
            for name in implementations:
                click.echo(f" - {name}")
            raise click.Abort()

        cls = implementations[builtin]
        cls().run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
