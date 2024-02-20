from PyQt5.QtWidgets import QLabel,QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt
from vincirecipereader import XMLReader,Step,Recipe
import os
import xml.etree.ElementTree as ET
from mainwidget import MainWidget
class ActionsWidget(MainWidget,QWidget):
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
        self.editor.addTab()
        self.messageChanged.emit("Created a new recipe")
    
    @pyqtSlot()
    def OpenRecipe(self):
        filePath=''
        filePath =  QFileDialog.getOpenFileName (None,'Recipe File',MainWidget.workingDir,("Subrecipe Files (*.uRCP);;Recipe Files (*.RCP)"))[0]
        if filePath !='':
            try:
                recipe = XMLReader.ReadRecipe(filePath)
                if(self.editor.isAlreadyOpen(recipe.name)):
                    self.editor.switchTo(recipe.name)
                    self.messageChanged.emit("{} was already opened".format(recipe.name))
                else:
                    self.editor.changeCurrentTab(recipe.steps,recipe.name)
                    self.messageChanged.emit("Opened {}".format(recipe.name))
            except XMLReader.ReadRecipeError as e:
                self.messageChanged.emit("Failed to open file: {}".format(e))
                pass
    
    @pyqtSlot()
    def SaveRecipe(self):
        try:
            path,extension = QFileDialog.getSaveFileName (None,'Recipe File',MainWidget.workingDir,("Subrecipe Files (*.uRCP);;Recipe Files (*.RCP)"))
            extension = extension.split('(')[1][1:-1]
            name = path.split('/')[-1][:-len(extension)] 
            if (path != ''):
                xsi="{http://www.w3.org/2001/XMLSchema-instance}"
                steps = self.editor.GetCurrentList()
                root = ET.Element('CParam_Recipe')
                tree = ET.ElementTree(root)
                
                #root.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
                root.set('xmlns:xsd',"http://www.w3.org/2001/XMLSchema")
                
                scriptName = ET.SubElement(root,'ScriptName')
                scriptName.text = name

                for step in steps:
                    if(type(step) == Step):
                        #Is a real step
                        _type = step.type
                        attr = step.attr
                        sub = ET.SubElement(root,'CollecStep')
                        sub.set(xsi+'type',_type)

                        for key in attr.keys():
                            subsub = ET.SubElement(sub,key)
                            subsub.text = attr[key]
                    elif(type(step)==Recipe):
                        #Is a subrecipe, add a XML mark to remember
                        sub = ET.SubElement(root,'CollecStep')
                        sub.set('subrecipe',step.path)
                            
                tree.write(path, encoding="utf-8", xml_declaration=True)
                self.editor.ChangeTitleofTab(name)
                self.messageChanged.emit("Recipe saved to {}".format(path)) 
            
        except (IndexError, FileNotFoundError) as e:
            self.messageChanged.emit("Failed to save: {}".format(e))

    @pyqtSlot()
    def ExportRecipe(self):
        path,extension = QFileDialog.getSaveFileName (None,'Recipe File',MainWidget.workingDir,("Recipe Files (*.RCP)"))
        if (path != ''):
            extension = extension.split('(')[1][1:-1]
            name = path.split('/')[-1][:-len(extension)]
            xsi="{http://www.w3.org/2001/XMLSchema-instance}"
            steps = self.editor.GetCurrentList()
            root = ET.Element('CParam_Recipe')
            tree = ET.ElementTree(root)
            
            #root.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
            root.set('xmlns:xsd',"http://www.w3.org/2001/XMLSchema")
            
            scriptName = ET.SubElement(root,'ScriptName')
            scriptName.text = name

            for step in steps:
                if(type(step) == Step):
                    #Is a real step
                    _type = step.type
                    attr = step.attr
                    sub = ET.SubElement(root,'CollecStep')
                    sub.set(xsi+'type',_type)

                    for key in attr.keys():
                        subsub = ET.SubElement(sub,key)
                        subsub.text = attr[key]
                elif(type(step)==Recipe):
                    #Is a subrecipe, find all steps and write them
                    for substep in step.steps:
                        #Is a real step
                        _type = substep.type
                        attr = substep.attr
                        sub = ET.SubElement(root,'CollecStep')
                        sub.set(xsi+'type',_type)

                        for key in attr.keys():
                            subsub = ET.SubElement(sub,key)
                            subsub.text = attr[key]
                        
            tree.write(path, encoding="utf-8", xml_declaration=True) 
            self.editor.ChangeTitleofTab(name)
            self.messageChanged.emit("Recipe exported to {}".format(path))
        else:
            self.messageChanged.emit("Failed to export, filename empty")

    