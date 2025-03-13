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
    currentUserChanged = pyqtSignal()
    WORKING_DIR = '.'
    PROCESS_INI_PATH = '.'
    PROCESS_INI_PATH_VAR = "PROCESS_INI_PATH"
    WORKING_DIR_VAR = "WORKING_DIR"
    target_symbols = [""]*8

    def savePrefs(self):
        with open("user.pref",'w') as file:
            json = {"Users":self.userPrefs,
                    "lastUser":self.currentUser,
                    self.PROCESS_INI_PATH_VAR:self.PROCESS_INI_PATH}
            file.write(dumps(json))

    def GetRegisteredUsers(self):
        return list(self.userPrefs.keys())

    def loadPrefs(self):
        try:
            with open("user.pref",'r') as f:
                json = load(f)
                for user in json["Users"].keys():
                    self.userPrefs[user] = json['Users'][user]
                #All users loaded from prefs
                #Load and activate the previous user
                if "lastUser" in json:
                    self.currentUser = json["lastUser"]
                else:
                    self.currentUser = list(json["Users"].keys())[0]
                self.activateUser(self.currentUser)
                if self.PROCESS_INI_PATH_VAR in json:self.SetProcessIniPath(json[self.PROCESS_INI_PATH_VAR])
        except (FileNotFoundError,JSONDecodeError,KeyError) as e:
            open("user.pref",'w').close()
            self.userPrefs = {"Default":{self.WORKING_DIR_VAR:'.'}}
            self.activateUser("Default")
            self.savePrefs()


    def activateUser(self,user):
        self.currentUser = user
        self.WORKING_DIR = self.userPrefs[user][self.WORKING_DIR_VAR]
        self.currentUserChanged.emit()

    def SetWorkingDir(self,newDir):
        self.WORKING_DIR = newDir
        self.userPrefs[self.currentUser][self.WORKING_DIR_VAR] = newDir 
        

    def SetProcessIniPath(self,path):
        self.PROCESS_INI_PATH = path
        self.ReadProcessIni()

    def ReadProcessIni(self):
        path = self.PROCESS_INI_PATH
        with open(path) as f:
            lines = f.readlines()
            i = 0
            for line in lines:
                if "_Symb" in line:
                    #Found a symbol
                    self.target_symbols[i] = line.split("=")[1][:-1]
                    i+=1


    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    