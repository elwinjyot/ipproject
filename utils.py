from rich.markdown import Markdown
from managers import BaseManager
import os
from pandas import read_csv, options
from pandas.errors import EmptyDataError
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from decorators import checkExistance
import json

'''
utils.py script contains a class `Tools`
consisting of all essential functions required
for the application to run.

 -  METHOD LIST
[1] Initialization
[2] Add family member
[3] Remove family member
[4] Edit family member
'''


class Tools(BaseManager):
    # Initialization
    def __init__(self):
        options.mode.chained_assignment = None
        self.console = Console()
        self.BASE = os.getcwd()
        self.filePath = os.path.join(self.BASE, 'database.csv')
        with open("./units.json", "r") as file:
            self.units = json.load(file)
            file.close()
        self.records = None

        if 'database.csv' not in os.listdir():
            self.console.print('[b yellow]No existing data found![/b yellow]')
            self.console.print('[b yellow]Creating new database...[/b yellow]')
            open(os.path.join(self.BASE, "database.csv"), "w").close()
            self.console.print('[b green]Done![/b green]')

        try:
            dbData = read_csv(self.filePath, index_col=False)
        except EmptyDataError:
            self.records = None
        else:
            dbData.index = dbData['p_id'].values
            dbData = dbData.drop('p_id', axis='columns')
            self.records = dbData

    def execute(self, cmd):
        iterable = iter(cmd.split(' '))
        exception = ['h', 'help', 'q', 'quit']
        base_cmd = next(iterable)

        if base_cmd in exception:
            if base_cmd == 'h' or base_cmd == 'help':
                self.help()
            elif base_cmd == 'q' or base_cmd == 'quit':
                self.saveRecords()
                return True
            else:
                self.console.print('[b red]Command not found![/b red]')
                self.help()
                return False
        else:
            if base_cmd == 'show':
                arg = next(iterable)
                if arg == 'all':
                    self.getAllMembers()
                else:
                    arg = self.validateArg(arg)
                    if arg:
                        self.getRecord(arg)
                    else:
                        self.console.print(
                            '[b red]Type the `ID` of the record![/b red]')
                        self.help()
            elif base_cmd == 'edit':
                arg = self.validateArg(next(iterable))
                if arg:
                    self.updateMember(arg)
                else:
                    self.console.print(
                        '[b red]Type the `ID` of the record![/b red]')
                    self.help()

            elif base_cmd == 'delete':
                arg = self.validateArg(next(iterable))
                if arg:
                    self.removeMember(arg)
                else:
                    self.console.print(
                        '[b red]Type the `ID` of the record![/b red]')
                    self.help()
            elif base_cmd == 'add':
                self.addMember(cmd.split(' ')[1:])

            else:
                self.console.print('[b red]Command not found![/b red]')
                return False

    # Display all members
    def getAllMembers(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", justify="center")
        table.add_column("Name", justify="left")
        rows = self.records.iterrows()

        for index, row in rows:
            table.add_row(
                f"[bold magenta]{str(index)}[/bold magenta]", f"[i]{row['NAME']}[/i]")

        self.console.print(table)

    # Display a specific record
    @checkExistance
    def getRecord(self, id):
        spcRec = self.records.loc[int(id)]
        cols = self.records.columns[7:len(self.records.columns) + 1]
        all_items = []
        for col in cols:
            color = None
            normals = self.units[col.upper()]["normals"]
            unit = self.units[col.upper()]['unit']
            if int(spcRec[col]) < normals[spcRec['SEX']][0]:
                color = "#ff3f21"
            elif int(spcRec[col]) > normals[spcRec['SEX']][1]:
                color = "#ff2626"
            else:
                color = "#2aeb31"

            all_items.append(
                Panel(f"[b {color}]{str(spcRec[col])} {unit}[/b {color}]", expand=True,
                      title=f"[yellow]{col.capitalize()}[/yellow]"),
            )

        self.console.print(Markdown('***'))
        self.console.print("[bold yellow]Personal Information[/bold yellow]")
        PERS_INFO = f'''
- Name: {spcRec['NAME']}
- Age : {spcRec['AGE']}
- Sex : {spcRec['SEX']}
- Blood Type: {spcRec['BLOOD TYPE']}ve
- DOB : {spcRec['DOB']}
- Last Checkup: {spcRec['LAST CHECKUP']}
- Doctors Review: {spcRec['DOCTORS REVIEW']}'''
        self.console.print(Markdown(PERS_INFO))
        self.console.print(Markdown('***'))
        self.console.print("[bold yellow]Record[/bold yellow]")
        self.console.print(
            "\n[bold #ff3f21]Low[/bold #ff3f21] | [bold #2aeb31]Normal[/bold #2aeb31] | [bold #ff2626]High[/bold #ff2626]\n")
        self.console.print(Columns(all_items))

    # Save records into database.csv file
    @checkExistance
    def saveRecords(self):
        self.console.print("[b yellow]Saving changes...[/b yellow]")
        self.records.insert(0, "p_id", self.records.index, True)
        self.records.to_csv(self.filePath, index=False)
        self.console.print("[b green]Done![/b green]")

    # Add family members to database
    @checkExistance
    def addMember(self, id):
        args = id
        newId = self.records.shape[0] + 1
        frameDict = {'NAME': 'NIL', 'AGE': 'NIL',
                     'SEX': 'NIL', 'BLOOD TYPE': 'NIL',
                     'DOB': 'NIL', 'LAST CHECKUP': 'NIL',
                     'DOCTORS REVIEW': 'NIL', 'GLUCOSE LEVEL': 0,
                     'CHOLESTROL LEVEL': 0, 'RBC COUNT': 0,
                     'WBC COUNT': 0, 'PLATELET COUNT': 0,
                     'HAEMOGLOBIN COUNT': 0}

        allKeys = []
        for arg in args:
            key = " ".join((arg.split('=')[0]).split('_')).upper()
            val = "".join(arg.split('=')[-1])
            allKeys.append(key)
            if key not in self.records.columns:
                self.console.print(f'[b red]Column "{key}" not valid![/b red]')
                return
            else:
                if key == 'SEX':
                    frameDict[key] = val.lower().capitalize()
                else:
                    frameDict[key] = val

        if 'NAME' not in allKeys or 'SEX' not in allKeys:
            self.console.print(f'[b red]Name and Sex is required![/b red]')
            return
        else:
            self.records.loc[newId] = frameDict
            self.console.print(
                f"[b green]Created new record for {frameDict['NAME']}.[/b green]")

    # Remove family members from database
    @checkExistance
    def removeMember(self, id):
        while True:
            self.console.print("[b yellow]\nWARNING: Not undoable[/b yellow]")
            confirm = input(
                f"Are you sure you want to delete {self.records.loc[id]['NAME']}'s record [y/n]? ").lower()
            if confirm == "y" or confirm == "yes":
                self.console.print(
                    f"[b yellow]Deleting record data of {self.records.loc[id]['NAME']}[/b yellow]")
                self.records.drop(id, axis=0, inplace=True)
                self.console.print("[b green]Done![/b green]")
                break
            elif confirm == "n" or confirm == "no":
                self.console.print(
                    "[b green]Canceled delete operation![/b green]")
                break
            else:
                self.console.print("[b red]Type y or n![/b red]")
                continue

    # Edit family member details
    @checkExistance
    def updateMember(self, id):
        self.getRecord(id)
        col_name = input("Field Name: ").upper()
        new_val = input("New Value: ")
        try:
            new_val = int(new_val)
        except:
            pass

        self.console.print("[bold yellow]Updating member...[/bold yellow]")
        self.records.loc[id, col_name] = new_val
        self.console.print("[bold green]Done![/bold green]")
