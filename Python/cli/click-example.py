import click


@click.group()
def entry_point():
    """Awesome app doing awesome things."""


@entry_point.command()
@click.option("--count", default=1, help="How much love you want")
@click.argument("name")
def spread(name, count):
    """Spread the love."""
    for i in range(count):
        print(f"{name} loves you ❤️")


@entry_point.command(name="print")
@click.argument("filepath", metavar="FILE", type=click.Path(exists=True))
@click.option("--show-meta", default=False, is_flag=True)
def print_(filepath, show_meta):
    """Print the file."""
    if show_meta:
        print(f"File path: {filepath}")
        print("-" * 80)
    with open(filepath, "r") as f:
        print(f.read())


if __name__ == "__main__":
    entry_point()
