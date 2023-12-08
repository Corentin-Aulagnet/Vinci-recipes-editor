from PyQt5.QtWidgets import QLabel,QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt
from vincirecipereader import XMLReader,Step,Recipe
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
        self.editor.ChangeTitle('')
    
    @pyqtSlot()
    def OpenRecipe(self):
        try :
            filePath =  QFileDialog.getOpenFileName (None,'Recipe File','C:/Users/p06173/Documents/PhD/Work/EXP/Recipes',("Subrecipe Files (*.uRCP);;Recipe Files (*.RCP)"))[0]
            recipe = XMLReader.ReadRecipe(filePath)
            self.editor.PopulateList(recipe.steps)
            self.editor.ChangeTitle(recipe.name)
        except FileNotFoundError:
            pass
    
    @pyqtSlot()
    def SaveRecipe(self):
        path,extension = QFileDialog.getSaveFileName (None,'Recipe File','C:/Users/p06173/Documents/PhD/Work/EXP/Recipes',("Subrecipe Files (*.uRCP);;Recipe Files (*.RCP)"))
        extension = extension.split('(')[1][1:-1]
        name = path.split('/')[-1][:-len(extension)] 
        if (path != ''):
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
                if(type(step) == Step):
                    #Is a real step
                    _type = step.type
                    attr = step.attr
                    print(_type)
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
        #else:
        #Write to satus bar

    @pyqtSlot()
    def ExportRecipe(self):
        path,extension = QFileDialog.getSaveFileName (None,'Recipe File','C:/Users/p06173/Documents/PhD/Work/EXP/Recipes',("Recipe Files (*.RCP)"))
        extension = extension.split('(')[1][1:-1]
        name = path.split('/')[-1][:-len(extension)]
        if (path != ''):
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
                if(type(step) == Step):
                    #Is a real step
                    _type = step.type
                    attr = step.attr
                    print(_type)
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
                        print(_type)
                        sub = ET.SubElement(root,'CollecStep')
                        sub.set(xsi+'type',_type)

                        for key in attr.keys():
                            subsub = ET.SubElement(sub,key)
                            subsub.text = attr[key]
                        
            tree.write(path, encoding="utf-8", xml_declaration=True) 
        #else:
        #Write to satus bar

    