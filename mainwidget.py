from PyQt5.QtCore import pyqtSignal
class MainWidget():
    messageChanged = pyqtSignal(str)
    workingDir = '.'

    @staticmethod
    def SetWorkingDir(newDir):
        MainWidget.workingDir = newDir
        with open("user.pref",'w') as file:
            file.write(MainWidget.workingDir)
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)