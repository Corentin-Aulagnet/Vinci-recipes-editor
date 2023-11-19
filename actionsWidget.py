from PyQt5.QtWidgets import QLabel,QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog
from PyQt5.QtCore import pyqtSlot,QObject,QSize
from vincirecipereader import XMLReader
import os
class ActionsWidget(QWidget):
    def __init__(self,editor,parent = None):
        super().__init__(parent)
        self.editor = editor
        self.layout = QVBoxLayout()

        self.createButton = QPushButton("Create Recipe")
        self.createButton.clicked.connect(self.CreateRecipe)
        self.layout.addWidget(self.createButton)

        self.openButton = QPushButton("Open Recipe")
        self.openButton.clicked.connect(self.OpenRecipe)
        self.layout.addWidget(self.openButton)

        self.saveButton = QPushButton("Save Recipe")
        self.saveButton.clicked.connect(self.SaveRecipe)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)

    @pyqtSlot()
    def CreateRecipe(self):
        raise NotImplementedError
    
    @pyqtSlot()
    def OpenRecipe(self):
        filePath =  QFileDialog.getOpenFileName (None,'Recipe File',os.getcwd())[0]
        recipe = XMLReader.ReadRecipe(filePath)
        self.editor.PopulateList(recipe.steps)
    
    @pyqtSlot()
    def SaveRecipe(self):
        print(self.editor.GetListItemData())
        

    