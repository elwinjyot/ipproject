from rich import console
from rich.console import Console

console = Console()


def checkExistance(func):
    def inner(self, id):
        if self.records:
            return func(self, id)
        else:
            console.print("[bold yellow]No records found 😕[/bold yellow]")

    return inner
