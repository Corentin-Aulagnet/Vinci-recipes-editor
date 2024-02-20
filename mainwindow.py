from PyQt5.QtWidgets import QMainWindow,QDockWidget,QAction,QWidget,QLabel,QFileDialog,QMessageBox
from PyQt5.QtCore import Qt,pyqtSignal
from librarywidget import LibraryWidget
from editorwidget import EditorWidget
from actionsWidget import ActionsWidget
from mainwidget import MainWidget
class MainWindow(QMainWindow):
    version = "v0.3.0"
    date= "20th of February, 2024"
    def __init__(self,width=1400,height=800):
        super().__init__()
        self.height = height
        self.width = width
        self.left = 100
        self.top = 100
        
        self.setWindowTitle("Vinci Recipe Editor")
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initWorkingDir()
        self.initMainLayout()
        self.initMenus()
        self.show()

    def initWorkingDir(self):
        try:
            with open("user.pref",'r') as f:
                MainWidget.SetWorkingDir(f.readline())
        except FileNotFoundError:
            pass
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
        ###Editor
        self.editWorkingPath_action = QAction("Set Working Directory...",self)
        self.editWorkingPath_action.triggered.connect(self.SetWorkingDir)
        self.prefMenu.addAction(self.editWorkingPath_action)
        ##About
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.version_action = QAction("Version",self)
        self.version_action.triggered.connect(self.DisplayVersion)
        self.aboutMenu.addAction(self.version_action)

    def DisplayVersion(self):
        QMessageBox.information(self,'Version',"""Version: {}\n
Date of publication: {}\n
Details: To be published""".format(MainWindow.version,MainWindow.date))
    def SetWorkingDir(self):
        dir = QFileDialog.getExistingDirectory(self,caption="Set Working Directory",directory = MainWidget.workingDir)
        if dir != "":
            MainWidget.SetWorkingDir(dir)
            self.PrintNormalMessage("Changed working directory to {}".format(MainWidget.workingDir))
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
        self.addDockWidget(Qt.LeftDockWidgetArea,self.libDock)

        self.editorDock = QDockWidget("Editor -")
        self.editorDock.setWidget(self.recipeEditorWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea,self.editorDock)

        self.actionsDock = QDockWidget("Actions")
        self.actionsDock.setWidget(self.actionsWidget)
        self.addDockWidget(Qt.RightDockWidgetArea,self.actionsDock)


    def PrintNormalMessage(self,message):
        self.statusBar().clearMessage()
        self.statusBar().showMessage(message)


    
