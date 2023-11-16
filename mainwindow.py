from PyQt5.QtWidgets import QMainWindow,QHBoxLayout,QAction,QWidget
from librarywidget import LibraryWidget

class MainWindow(QMainWindow):
    def __init__(self,width=1400,height=800):
        super().__init__()
        self.height = height
        self.width = width
        self.setWindowTitle("Vinci Recipe Editor")


        self.initMenus()
        self.initMainLayout()
        self.show()


    def initMenus(self):
        
        ##Window Menu
        self.windowMenu = self.menuBar().addMenu("&Windows")
        ###plots
        #self.plot_dock_action = QAction("Graphs",self)
        #self.windowMenu.addAction(self.plotDock.toggleViewAction())
        ##About
        self.aboutMenu = self.menuBar().addMenu("&About")

    def initMainLayout(self):

        self.setCentralWidget(QWidget())
        #Layout definition
        self.mainLayout = QHBoxLayout()

        #Leftmost widget is a library of user defined recipes, with a button to add recipes to the library
        self.libraryWidget = LibraryWidget()
        ##Center widget is the recipe being edited as a list of small clickable,dragable rectangles
        #self.recipeEditorWidget = recipeEditorWidget()
        ##Rightmost widget is a column of action button : add a step, remove a step, open a recipe, delete the recipe, save the recipe
        #self.actionsWidget = actionsWidget()

        self.mainLayout.addWidget(self.libraryWidget)

        self.centralWidget().setLayout(self.mainLayout)
