from PyQt5.QtWidgets import QMainWindow,QDockWidget,QAction,QWidget
from PyQt5.QtCore import Qt
from librarywidget import LibraryWidget
from editorwidget import RecipeEditorWidget
from actionsWidget import ActionsWidget
class MainWindow(QMainWindow):
    def __init__(self,width=1400,height=800):
        super().__init__()
        self.height = height
        self.width = width
        self.left = 100
        self.top = 100
        self.setWindowTitle("Vinci Recipe Editor")
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initMenus()
        self.initMainLayout()
        self.show()


    def initMenus(self):
        
        ##Window Menu
        self.windowMenu = self.menuBar().addMenu("&Windows")
        ##About
        self.aboutMenu = self.menuBar().addMenu("&About")

    def initMainLayout(self):

        self.setCentralWidget(QWidget())

        #Leftmost widget is a library of user defined recipes, with a button to add recipes to the library
        self.libraryWidget = LibraryWidget(parent=self)
        ##Center widget is the recipe being edited as a list of small clickable,dragable rectangles
        self.recipeEditorWidget = RecipeEditorWidget(parent = self)
        ##Rightmost widget is a column of action button : add a step, remove a step, open a recipe, delete the recipe, save the recipe
        self.actionsWidget = ActionsWidget(parent = self,editor=self.recipeEditorWidget)

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

