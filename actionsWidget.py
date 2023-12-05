from PyQt5.QtWidgets import QLabel,QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt
from vincirecipereader import XMLReader,Step
import os
import xml.etree.ElementTree as ET
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

        self.exportButton = QPushButton("Export Recipe")
        self.exportButton.clicked.connect(self.ExportRecipe)
        self.layout.addWidget(self.exportButton)

        self.setLayout(self.layout)

    @pyqtSlot()
    def CreateRecipe(self):
        self.editor.clear()
    
    @pyqtSlot()
    def OpenRecipe(self):
        filePath =  QFileDialog.getOpenFileName (None,'Recipe File',os.getcwd())[0]
        recipe = XMLReader.ReadRecipe(filePath)
        self.editor.PopulateList(recipe.steps)
    
    @pyqtSlot()
    def SaveRecipe(self):
        name = QFileDialog.getSaveFileName (None,'Recipe File',os.getcwd(),("Recipe Files (*.RCP)"))[0]
        if (name != ''):
            xsi="{http://www.w3.org/2001/XMLSchema-instance}"
            steps = self.editor.GetListItemData()
            print(steps)
            root = ET.Element('CParam_Recipe')
            tree = ET.ElementTree(root)
            
            #root.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
            root.set('xmlns:xsd',"http://www.w3.org/2001/XMLSchema")
            
            scriptName = ET.SubElement(root,'ScriptName')
            scriptName.text = name

            for step in steps:
                _type = step.type
                attr = step.attr
                print(_type)
                sub = ET.SubElement(root,'CollecStep')
                sub.set(xsi+'type',_type)

                for key in attr.keys():
                    subsub = ET.SubElement(sub,key)
                    subsub.text = attr[key]
                        
            tree.write(name, encoding="utf-8", xml_declaration=True) 
        #else:
        #Write to satus bar

    @pyqtSlot()
    def ExportRecipe(self):
        name = QFileDialog.getSaveFileName (None,'Recipe File',os.getcwd(),("Recipe Files (*.RCP)"))[0]
        if (name != ''):
            xsi="{http://www.w3.org/2001/XMLSchema-instance}"
            steps = self.editor.GetListItemData()
            print(steps)
            root = ET.Element('CParam_Recipe')
            tree = ET.ElementTree(root)
            
            #root.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
            root.set('xmlns:xsd',"http://www.w3.org/2001/XMLSchema")
            
            scriptName = ET.SubElement(root,'ScriptName')
            scriptName.text = name

            for step in steps:
                _type = step.type
                attr = step.attr
                print(_type)
                sub = ET.SubElement(root,'CollecStep')
                sub.set(xsi+'type',_type)

                for key in attr.keys():
                    subsub = ET.SubElement(sub,key)
                    subsub.text = attr[key]
                        
            tree.write(name, encoding="utf-8", xml_declaration=True) 
        #else:
        #Write to satus bar

    