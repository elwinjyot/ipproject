from rich.tree import Tree
from rich.text import Text


class BaseManager:
    def help(self):
        show = Tree("[bold yellow]show[/bold yellow]")
        show.add("all - [i]shows all added members[/i]")
        show.add("<id> - [i]shows details of member with specified id[/i]")

        edit = Tree("[bold yellow]edit[/bold yellow]")
        edit.add("<id> - [i]edit information of a member")

        delete = Tree("[bold yellow]delete[/bold yellow]")
        delete.add("<id> - [i]delete member with this id")

        add = Tree("[bold yellow]add[/bold yellow]")
        add.add(Tree("[bold magenta]name[/bold magenta]"))
        add.add(Tree("[bold magenta]age[/bold magenta]"))
        add.add(Tree("[bold magenta]sex[/bold magenta]"))
        add.add(Tree("[bold magenta]dob[/bold magenta]"))
        add.add(Tree("[bold magenta]blood_type[/bold magenta]"))
        add.add(Tree("[bold magenta]last_checkup[/bold magenta]"))
        add.add(Tree("[bold magenta]doctors_review[/bold magenta]"))
        add.add(Tree("[bold magenta]glucose_level[/bold magenta]"))
        add.add(Tree("[bold magenta]cholestrol_level[/bold magenta]"))
        add.add(Tree("[bold magenta]rbc_count[/bold magenta]"))
        add.add(Tree("[bold magenta]wbc_count[/bold magenta]"))
        add.add(Tree("[bold magenta]platelet_count[/bold magenta]"))
        add.add(Tree("[bold magenta]haemoglobin_count[/bold magenta]"))

        self.console.print(Text("Commands", style="bold magenta"))
        self.console.print(show)
        self.console.print("\n", edit)
        self.console.print("\n", delete)
        self.console.print("\n", add)

    def validateArg(self, arg):
        try:
            arg = int(arg)
        except ValueError:
            return None
        else:
            return arg
