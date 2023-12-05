from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QListWidgetItem
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt

import os
from vincirecipereader import XMLReader
class LibraryWidget(QWidget):
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

        self.addToLibraryButton = QPushButton("Add a recipe")
        self.addToLibraryButton.clicked.connect(self.AddToLibraryAction)
        self.layout.addWidget(self.addToLibraryButton)
        
        self.setLayout(self.layout)
        
    
    def ReadCustomSubRecipes(self):
        try :
            with open("SubRecipes.dat",'r') as file:
                lines = file.readlines()
                for line in lines:
                    self.customSubRecipes.append(XMLReader.ReadRecipe(line[:-1]))
        except FileNotFoundError:
            print("file not found")
            f = open("SubRecipes.dat",'w')
            f.close()
            self.ReadCustomSubRecipes()
    @pyqtSlot()
    def AddToLibraryAction(self):
        filePath =  QFileDialog.getOpenFileName (None,'Recipe File',os.getcwd())[0]
        recipe = XMLReader.ReadRecipe(filePath)
        self.customSubRecipes.append(recipe)
        item = QListWidgetItem()
        item.setText(recipe.name)
        item.setData(Qt.UserRole,recipe)
        self.listWidget.addItem(item)
        with open("SubRecipes.dat",'a') as file:
            file.write(filePath+"\n")
        self.PopulateList()

    def PopulateList(self):
        self.listWidget.clear()
        for sub in self.customSubRecipes:
            item = QListWidgetItem()
            item.setText(sub.name)
            item.setData(Qt.UserRole,sub)
            self.listWidget.addItem(item)

    def debugPopulateList(self):
        for i in range(2):
            self.listWidget.addItem("Item {}".format(i))



class MyLibraryList(QListWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
