from rich.tree import Tree
from rich.text import Text

class BaseManager:
    def help(self):
        show = Tree("[bold yellow]show[/bold yellow]")
        show.add("all - [i]shows all added members[/i]")
        show.add("<id> - [i]shows details of member with specified id[/i]")

        edit = Tree("[bold yellow]edit[/bold yellow]")
        edit.add("<id> <info> - [i]edit information of a member | <info> should be replaced with column to be edited[/i]")

        self.console.print(Text("Commands", style="bold magenta"))
        print("")
        self.console.print(show)
        print("")
        self.console.print(edit)


    def validateArg(self, arg):
        try:
            arg = int(arg)
        except ValueError:
            return None
        else:
            return arg 