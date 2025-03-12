from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QListWidgetItem,QHBoxLayout
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt
from PyQt5.QtGui import QIcon
from mainwidget import MainWidget
from editorwidget import EditorWidget
from editor import MyTableView
import os
from vincirecipereader import XMLReader
class LibraryWidget(MainWidget,QWidget):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.customSubRecipes=[]
        self.ReadCustomSubRecipes()
        

        self.layout = QVBoxLayout()
        self.listWidget= QListWidget()
        self.listWidget.setDragDropMode(QAbstractItemView.DragOnly)
        self.listWidget.setSortingEnabled(True)
        
        self.PopulateList()
        
        self.layout.addWidget(self.listWidget)

        self.buttonsLayout = QHBoxLayout()

        self.addToLibraryButton = QPushButton("Add a recipe")
        self.addToLibraryButton.clicked.connect(self.AddToLibraryAction)
        self.buttonsLayout.addWidget(self.addToLibraryButton)

        self.addToRecipeButton = QPushButton('+')
        self.addToRecipeButton.clicked.connect(self.AddToRecipeAction)
        self.buttonsLayout.addWidget(self.addToRecipeButton)

        self.layout.addLayout(self.buttonsLayout)
        
        self.setLayout(self.layout)
        
    
    def ReadCustomSubRecipes(self):
        try :
            with open("SubRecipes.dat",'r') as file:
                lines = file.readlines()
                for line in lines:
                    self.customSubRecipes.append(XMLReader.ReadRecipe(line[:-1]))
        except FileNotFoundError:
            f = open("SubRecipes.dat",'w')
            f.close()
            self.ReadCustomSubRecipes()
    @pyqtSlot()
    def AddToLibraryAction(self):
        filePath =  QFileDialog.getOpenFileName (None,'Recipe File',self.WORKING_DIR,("Recipe Files (*.RCP);;Subrecipe Files (*.uRCP)"))[0]
        try:
            recipe = XMLReader.ReadRecipe(filePath)
            
            self.customSubRecipes.append(recipe)
            with open("SubRecipes.dat",'a') as file:
                file.write(filePath+"\n")
            self.PopulateList()
        except XMLReader.ReadRecipeError:
                #Error during reading, file does not exists
                self.messageChanged.emit("Failed to add subrecipe to the library")

    @pyqtSlot()
    def AddToRecipeAction(self):
        selectedRecipe = self.listWidget.item(self.listWidget.currentRow()).data(Qt.UserRole)
        view = EditorWidget.currentWidget.view
        if(len(view.selectedIndexes())>0):
            view.insertRow(view.selectedIndexes()[0].row()+1,selectedRecipe)
        else :
            view.addRow(selectedRecipe)


    def PopulateList(self):
        self.listWidget.clear()
        for sub in self.customSubRecipes:
            item = self.CreateItem(sub)
            self.listWidget.addItem(item)

    def CreateItem(self,recipe):
        item = QListWidgetItem()
        item.setText(recipe.name)
        item.setData(Qt.UserRole,recipe)
        icon = QIcon('res/ass_512.png')
        item.setIcon(icon)
        return item

    def debugPopulateList(self):
        for i in range(2):
            self.listWidget.addItem("Item {}".format(i))



class MyLibraryList(QListWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
    
    '''def dragEvent(self,event:QDragEvent):
        drag = QDrag()'''
