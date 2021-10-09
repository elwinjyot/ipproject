import os

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

class Tools:
    # Initialization
    def __init__(self):
        self.BASE = os.getcwd()
        self.filePath = os.path.join(self.BASE, 'database.csv')
        
        if 'database.csv' not in os.listdir():
            open(os.path.join(self.BASE, "database.csv"), "w").close()

    # Add family members to database
    def addMember(self):
        pass

    # Remove family members from database
    def removeMember(self):
        pass

    # Edit family member details
    def updateMember(self):
        pass

    # Plot monthly report
    def plotGraph(self):
        pass
