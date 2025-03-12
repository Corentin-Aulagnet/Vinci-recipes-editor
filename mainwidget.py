from PyQt5.QtCore import pyqtSignal
from json import dumps,load,JSONDecodeError
class MainWidget(object):
    _shared_borg_state = {}
  
    def __new__(cls, *args, **kwargs):
        obj = super(MainWidget, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_borg_state
        return obj
    userPrefs = {}
    currentUser = ''
    messageChanged = pyqtSignal(str)
    currentUserChanged = pyqtSignal(str)
    WORKING_DIR = '.'
    PROCESS_INI_PATH = '.'
    PROCESS_INI_PATH_VAR = "PROCESS_INI_PATH"
    WORKING_DIR_VAR = "WORKING_DIR"
    target_symbols = [""]*8
    @staticmethod 
    def savePrefs():
        with open("user.pref",'w') as file:
            json = {"Users":MainWidget.userPrefs,
                    "lastUser":MainWidget.currentUser,
                    MainWidget.PROCESS_INI_PATH_VAR:MainWidget.PROCESS_INI_PATH}
            file.write(dumps(json))
    @staticmethod 
    def GetRegisteredUsers():
        return list(MainWidget.userPrefs.keys())
    @staticmethod
    def loadPrefs():
        try:
            with open("user.pref",'r') as f:
                json = load(f)
                for user in json["Users"].keys():
                    MainWidget.userPrefs[user] = json['Users'][user]
                #All users loaded from prefs
                #Load and activate the previous user
                if "lastUser" in json:
                    MainWidget.currentUser = json["lastUser"]
                else:
                    MainWidget.currentUser = list(json["Users"].keys())[0]
                MainWidget.activateUser(MainWidget.currentUser)
                if MainWidget.PROCESS_INI_PATH_VAR in json:MainWidget.SetProcessIniPath(json[MainWidget.PROCESS_INI_PATH_VAR])
        except (FileNotFoundError,JSONDecodeError) as e:
            pass
    @staticmethod
    def activateUser(user):
        MainWidget.currentUser = user
        MainWidget.WORKING_DIR = MainWidget.userPrefs[user][MainWidget.WORKING_DIR_VAR]
        MainWidget.currentUserChanged.emit("user")
    @staticmethod
    def SetWorkingDir(newDir):
        MainWidget.WORKING_DIR = newDir
        MainWidget.userPrefs[MainWidget.currentUser][MainWidget.WORKING_DIR_VAR] = newDir 
        
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
    