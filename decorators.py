from rich import console
from rich.console import Console

console = Console()


def checkExistance(func):
    def inner(self, id=None):
        if self.records is not None:
            if id:
                return func(self, id)
            else:
                return func(self)
        else:
            console.print("[bold yellow]No records found 😕[/bold yellow]")

    return inner
