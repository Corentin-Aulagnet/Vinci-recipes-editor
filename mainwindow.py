from PyQt5.QtWidgets import QApplication,QMainWindow,QDockWidget,QAction,QWidget,QLabel,QFileDialog,QMessageBox
from PyQt5.QtCore import Qt,pyqtSlot
from PyQt5.QtGui import QIcon
from librarywidget import LibraryWidget
from editorwidget import EditorWidget
from actionsWidget import ActionsWidget
from mainwidget import MainWidget
from manageUsersWindow import ManageUsersWindow
import os,sys
from updateCheck import UpdateCheckThread,start_update

class MainWindow(MainWidget,QMainWindow):
    version = "v0.10.0"
    date= "12th of March, 2025"
    github_user = 'Corentin-Aulagnet'
    github_repo = 'Vinci-recipes-editor'
    asset_name= lambda s : f'VinciRecipeEditor_{s}_python3.8.zip'
    def __init__(self,width=1400,height=800):
        super().__init__()
        self.height = height
        self.width = width
        self.left = 100
        self.top = 100
        
        self.setWindowTitle("Vinci Recipe Editor")
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setIcon("res\VinciRecipeEditor.ico")
        self.setWindowIcon(QIcon("res\VinciRecipeEditor.ico"))
        MainWidget.loadPrefs()
        self.initMainLayout()
        self.initMenus()
        self.checkForUpdates()
        self.show()

    def checkForUpdates(self):
        #Check for updates
        # Start the update check thread
        self.update_thread = UpdateCheckThread(MainWindow.github_user,MainWindow.github_repo,MainWindow.version,MainWindow.asset_name)
        self.update_thread.update_available.connect(self.on_update_check_finished)
        self.update_thread.start()
    @pyqtSlot(str)
    def on_update_check_finished(self,latest_version):
        #Get the folder where the app is running from
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        installation_folder = application_path
        if latest_version != '':
            msgBox = QMessageBox()
            msgBox.setText(f"A newer version ({latest_version}) is available. You are currently using version {MainWindow.version}.");
            msgBox.setInformativeText("Do you want to download the latest version? VinciRecipesEditor will be closed")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.Yes)
            ret = msgBox.exec()
            if ret == QMessageBox.Yes : 
                start_update(latest_version,installation_folder,MainWindow.github_user,MainWindow.github_repo,MainWindow.asset_name(latest_version))
                QApplication.instance().quit()
    
    def initMenus(self):
        
        ##Window Menu
        self.window_menu = self.menuBar().addMenu("&Windows")

        ###Library
        self.libDock_action = QAction("Library",self)
        self.window_menu.addAction(self.libDock.toggleViewAction())

        ###Editor
        self.editorDock_action = QAction("Editor",self)
        self.window_menu.addAction(self.editorDock.toggleViewAction())

        ###Actions
        self.actionsDock_action = QAction("Actions",self)
        self.window_menu.addAction(self.actionsDock.toggleViewAction())

        ##Preferences
        self.prefMenu = self.menuBar().addMenu("&Preferences")
        ###Working directory
        self.editWorkingPath_action = QAction("Set Working Directory...",self)
        self.editWorkingPath_action.triggered.connect(self.SetWorkingDir)
        self.prefMenu.addAction(self.editWorkingPath_action)
        ###PROCESS.INI
        self.editprocessini_action = QAction("Choose PROCESS.INI file",self)
        self.editprocessini_action.triggered.connect(self.SetProcessIni)
        self.prefMenu.addAction(self.editprocessini_action)

        ##Users
        self.usersMenu = self.menuBar().addMenu("&Users")
        ###Manage Users
        self.manageUsers_action = QAction("Manage Users",self)
        self.manageUsers_action.triggered.connect(self.OpenManageUsersWindow)
        self.usersMenu.addAction(self.manageUsers_action)
        ##About
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.version_action = QAction("Version",self)
        self.version_action.triggered.connect(self.DisplayVersion)
        self.aboutMenu.addAction(self.version_action)

    def OpenManageUsersWindow(self):
        self.manageUsersWindow = ManageUsersWindow()

    def DisplayVersion(self):
        msgBox = QMessageBox(self)
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setWindowTitle('About')
        msgBox.setText("""Version: {}\r
Date of publication: {}\r
Details: Developped and maintained by Corentin Aulagnet.\r
You can publish new issues on <a href=\'https://github.com/Corentin-Aulagnet/Vinci-recipes-editor/issues'>GitHub</a>""".format(MainWindow.version,MainWindow.date))
        msgBox.exec()
    def SetWorkingDir(self):
        dir = QFileDialog.getExistingDirectory(self,caption="Set Working Directory",directory = self.WORKING_DIR)
        if dir != "":
            MainWidget.SetWorkingDir(dir)
            MainWidget.savePrefs()
            self.PrintNormalMessage("Changed working directory to {}".format(self.WORKING_DIR))
    
    def SetProcessIni(self):
            path = QFileDialog.getOpenFileName(self,caption="Find PROCESS.INI",directory = self.WORKING_DIR)[0]
            if path != "":
                MainWidget.SetProcessIniPath(path)
                MainWidget.savePrefs()
                self.PrintNormalMessage("Changed PROCESS.INI to {}".format(MainWidget.PROCESS_INI_PATH))

    def initMainLayout(self):

        self.setCentralWidget(QWidget())

        #Leftmost widget is a library of user defined recipes, with a button to add recipes to the library
        self.libraryWidget = LibraryWidget(parent=self)
        ##Center widget is the recipe being edited as a list of small clickable,dragable rectangles
        self.recipeEditorWidget = EditorWidget(parent = self)
        ##Rightmost widget is a column of action button : add a step, remove a step, open a recipe, delete the recipe, save the recipe
        self.actionsWidget = ActionsWidget(parent = self,editor=self.recipeEditorWidget)

        self.libraryWidget.messageChanged.connect(self.PrintNormalMessage)
        self.recipeEditorWidget.messageChanged.connect(self.PrintNormalMessage)
        self.actionsWidget.messageChanged.connect(self.PrintNormalMessage)

        self.setCentralWidget(QWidget())
        self.centralWidget().hide()

        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.ForceTabbedDocks | QMainWindow.AllowNestedDocks)


        self.libDock = QDockWidget("Library")
        self.libDock.setWidget(self.libraryWidget)

        self.editorDock = QDockWidget("Editor")
        self.editorDock.setWidget(self.recipeEditorWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.libDock)

       
        self.tabifyDockWidget(self.libDock,self.editorDock)

        
        

        self.actionsDock = QDockWidget("Actions")
        self.actionsDock.setWidget(self.actionsWidget)
        self.addDockWidget(Qt.RightDockWidgetArea,self.actionsDock)


    def PrintNormalMessage(self,message):
        self.statusBar().clearMessage()
        self.statusBar().showMessage(message)


    
