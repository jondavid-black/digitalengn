import click
from importlib.metadata import version, PackageNotFoundError


def get_version():
    try:
        return version("engn")
    except PackageNotFoundError:
        return "unknown"


@click.group()
@click.version_option(
    version=get_version(), prog_name="engn", help="Show the version and exit."
)
def main():
    """ENGN CLI for AI agent integration."""
    pass


if __name__ == "__main__":
    main()
