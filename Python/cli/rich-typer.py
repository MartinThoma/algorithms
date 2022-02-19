import typer
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax


def app(filepath: Path = typer.Option(..., exists=True)):
    """Print a python file."""
    with open(filepath, "r") as f:
        code = f.read()
    syntax = Syntax(code, "python", theme="solarized-dark", line_numbers=True)
    console = Console()
    console.print(syntax)


if __name__ == "__main__":
    typer.run(app)
