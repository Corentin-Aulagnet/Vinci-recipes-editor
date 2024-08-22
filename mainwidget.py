from PyQt5.QtCore import pyqtSignal
from json import dumps
class MainWidget():
    messageChanged = pyqtSignal(str)
    workingDir = '.'
    PROCESS_INI_PATH = '.'
    target_symbols = [""]*8
    @staticmethod 
    def savePrefs():
        with open("user.pref",'w') as file:
            json = {"WORKING_DIR" : "{}".format(MainWidget.workingDir),
                    "PROCESS_INI_PATH": "{}".format(MainWidget.PROCESS_INI_PATH)}
            file.write(dumps(json))
    
    @staticmethod
    def SetWorkingDir(newDir):
        MainWidget.workingDir = newDir 
        
    @staticmethod
    def SetProcessIniPath(path):
        MainWidget.PROCESS_INI_PATH = path
        MainWidget.ReadProcessIni()
    @staticmethod
    def ReadProcessIni():
        path = MainWidget.PROCESS_INI_PATH
        with open(path) as f:
            lines = f.readlines()
            i = 0
            for line in lines:
                if "_Symb" in line:
                    #Found a symbol
                    MainWidget.target_symbols[i] = line.split("=")[1][:-1]
                    i+=1


    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    