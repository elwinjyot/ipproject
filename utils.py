from pandas.core.indexes import base
from rich import console
from rich.markdown import Markdown
from managers import BaseManager
import os
import pandas as pd
from pandas.errors import EmptyDataError
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from decorators import checkExistance

'''
utils.py script contains a class `Tools`
consisting of all essential functions required
for the application to run.

 -  METHOD LIST
[1] Initialization
[2] Add family member
[3] Remove family member
[4] Edit family member
[5] Plot monthly report'''


class Tools(BaseManager):
    # Initialization
    def __init__(self):
        self.console = Console()
        self.BASE = os.getcwd()
        self.filePath = os.path.join(self.BASE, 'database.csv')
        self.records = None

        if 'database.csv' not in os.listdir():
            open(os.path.join(self.BASE, "database.csv"), "w").close()

        try:
            dbData = pd.read_csv(self.filePath)
        except EmptyDataError:
            self.records = None
        else:
            if dbData.empty:
                self.records = None
            else:
                recDFIndex = dbData['id'].values
                dbData.index = recDFIndex
                dbData = dbData.drop('id', axis='columns')
                self.records = dbData

    def execute(self, cmd):
        iterable = iter(cmd.split(' '))
        exception = ['h', 'help', 'q', 'quit']
        base_cmd = next(iterable)

        if base_cmd in exception:
            if base_cmd == 'h' or base_cmd == 'help':
                self.help()
            elif base_cmd == 'q' or base_cmd == 'quit':
                return True
            else:
                self.console.print('[b red]Command not found![/b red]')
                self.help()
                return False
        else:
            if base_cmd == 'show':
                arg = next(iterable)
                if arg == 'all':
                    self.getAllRecords()
                else:
                    arg = self.validateArg(arg) 
                    if arg is not None:
                        self.getRecord(arg)
                    else:
                        self.console.print('[b red]Command not found![/b red]')
                        self.help()
            else:
                self.console.print('[b red]Command not found![/b red]')
                return False

    # Display all records
    def getAllRecords(self):
        if self.records is None:
            self.console.print("[b yellow]No records found[/b yellow] 😕")
        else:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", justify="center")
            table.add_column("Name", justify="left")
            rows = self.records.iterrows()

            for index, row in rows:
                table.add_row(
                    f"[bold magenta]{str(index)}[/bold magenta]", f"[i]{row['Name']}[/i]")

            self.console.print(table)

    # Display a specific record
    @checkExistance
    def getRecord(self, id):
        spcRec = self.records.loc[int(id)]
        cols = self.records.columns[5:len(self.records.columns) + 1]
        all_items = []
        for col in cols:
            all_items.append(
                Panel(f"[b]{str(spcRec[col])}[/b]", expand=True, title=f"[yellow]{col}[/yellow]"),
            )
        
        self.console.print(Markdown('***'))
        self.console.print("[bold yellow]Personal Information[/bold yellow]")
        PERS_INFO = f'''
- Name --> {spcRec['Name']}
- Age  --> {spcRec['Age']}
- Sex  --> {spcRec['Sex']}
- DOB  --> {spcRec['DOB']}
- Last Checkup --> {spcRec['Last Checkup']}'''
        self.console.print(Markdown(PERS_INFO))
        self.console.print(Markdown('***'))
        self.console.print("[bold yellow]Record[/bold yellow]")
        self.console.print(Columns(all_items))

    # Save records into database.csv file
    @checkExistance
    def saveRecords(self, data):
        data.to_csv(self.filePath)

    # Add family members to database
    @checkExistance
    def addMember(self):
        pass

    # Remove family members from database
    @checkExistance
    def removeMember(self):
        pass

    # Edit family member details
    @checkExistance
    def updateMember(self, id):
        pass

    # Plot monthly report
    @checkExistance
    def plotGraph(self):
        pass
