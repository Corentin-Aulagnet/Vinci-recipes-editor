from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
class MainWidget(QWidget):
    messageChanged = pyqtSignal(str)
    workingDir = '.'

    @staticmethod
    def SetWorkingDir(newDir):
        MainWidget.workingDir = newDir
        with open("user.pref",'w') as file:
            file.write(MainWidget.workingDir)
        
    def __init__(self,parent=None):
        super().__init__(parent)