import typer
from pathlib import Path

app = typer.Typer(help="Awesome app doing awesome things.", add_completion=False)


@app.command()
def spread(name: str, count: int = typer.Option(1, help="How much love you want")):
    """Spread the love."""
    for i in range(count):
        print(f"{name} loves you ❤️")


@app.command(name="print")
def print_(filepath: Path = typer.Option(..., exists=True), show_meta: bool = False):
    """Print the file."""
    if show_meta:
        print(f"File path: {filepath}")
        print("-" * 80)
    with open(filepath, "r") as f:
        print(f.read())


if __name__ == "__main__":
    app()
