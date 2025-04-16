"""Command-line interface for rack."""

import click

from rack.utils import discover_websites


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
def main() -> None:
    """Command-line interface for the Rack package."""


@main.command("list-builtins")
def list_builtins() -> None:
    """Lists all built-in Website implementations."""
    click.echo("Available built-in website implementations:")
    for cls in discover_websites():
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
def run(builtin: str, host: str, port: int, debug: bool, test: bool) -> None:
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
        implementations = {cls.__name__: cls for cls in discover_websites()}
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
