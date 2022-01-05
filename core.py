from rich.console import Console
from rich.markdown import Markdown
from utils import Tools


def main():
    console = Console()
    tools = Tools()
    
    INTRO_MD = f'''
# Medical Record Manager

Built and Managed by:
- Akash Kumar
- Mohit Tanwar
- Elwin Jyothis

>Type h or help for help.

>Type q or quit to quit application.
'''

    console.print(Markdown(INTRO_MD))

    running = True
    
    while running:
        try:
            command = input("\n👉 ")
        except KeyboardInterrupt:
            running = False
        else:
            ret = tools.execute(cmd=command)
            if ret:
                running = False
            else:
                continue


    console.print("[bold yellow]Have a nice day.[/bold yellow] :wave:")

if __name__ == '__main__':
    main()