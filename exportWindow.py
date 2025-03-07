from mainwidget import MainWidget
from PyQt5.QtWidgets import QApplication,QDialog,QVBoxLayout,QHBoxLayout,QLabel,QStyle,QPushButton,QLineEdit,QFileDialog,QCheckBox 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import xml.etree.ElementTree as ET
from vincirecipereader import Step,Recipe
import os
import shutil
class ExportWindow(MainWidget,QDialog):
    def __init__(self,currentRecipeName,editor,parent=None):
        super().__init__(parent)
        self.editor = editor
        self.currentRecipeName = currentRecipeName
        self.currentRecipePath= MainWidget.workingDir
        self.datalogFolderPath = ""
        self.setModal(True)
        self.setWindowTitle("Export Recipe")
        self.setWindowIcon(QIcon("res/floppy-disk-48.png"))
        #Define the layout
        self.mainLayout = QVBoxLayout(self)
        #Adds an horizontal layout for the recipe file
        self.filePathLayout = QHBoxLayout()
        self.filePathWidgets={"label":None,"textEdit":None,"button":None}
        label =  QLabel("Filepath")
        self.filePathWidgets["label"] = label
        textInput = QLineEdit()
        textInput.setReadOnly(True)
        self.filePathWidgets["textEdit"] = textInput
        button = QPushButton(icon=QApplication.style().standardIcon(QStyle.SP_FileIcon))
        button.clicked.connect(self.OpenFilePathWindow)
        self.filePathWidgets["button"] = button
        for key in self.filePathWidgets.keys():
            self.filePathLayout.addWidget(self.filePathWidgets[key])
        self.mainLayout.addLayout(self.filePathLayout)
        
        #Adds a CheckBox to choose the copy/no copy
        self.copyCheckBox = QCheckBox("Copy to datalog folder")
        self.copyCheckBox.stateChanged.connect(self.copyLayoutSetActive)
        self.mainLayout.addWidget(self.copyCheckBox)

        #Adds an horizontal layout for the recipe file
        self.datalogFolderLayout = QHBoxLayout()
        self.datalogFolderWidgets={"label":None,"textEdit":None,"button":None}
        label =  QLabel("Datalog Folder")
        self.datalogFolderWidgets["label"] = label
        textInput = QLineEdit()
        textInput.setReadOnly(True)
        textInput.setText(self.currentRecipeName)
        self.datalogFolderWidgets["textEdit"] = textInput
        button = QPushButton(icon=QApplication.style().standardIcon(QStyle.SP_DirIcon))
        button.clicked.connect(self.OpenFolderPathWindow)
        self.datalogFolderWidgets["button"] = button
        for key in self.datalogFolderWidgets.keys():
            self.datalogFolderLayout.addWidget(self.datalogFolderWidgets[key])
            self.datalogFolderWidgets[key].setEnabled(False)#Disable the widgets at start
        self.mainLayout.addLayout(self.datalogFolderLayout)

        #Add a button to confirm the export
        self.exportButton = QPushButton("Export")
        self.exportButton.clicked.connect(self.export)
        self.mainLayout.addWidget(self.exportButton)
        self.setLayout(self.mainLayout)
        self.show()
    def OpenFilePathWindow(self):
        path,extension = QFileDialog.getSaveFileName(None,'Recipe File',self.currentRecipeName,("Recipe Files (*.RCP)"))
        if path!="":
            l = path.split('/')
            name = l[-1]
            path = path[:-len(name)]
            self.currentRecipeName = name
            self.currentRecipePath = path
            self.filePathWidgets["textEdit"].setText(path+name)
    
    def OpenFolderPathWindow(self):
        path = QFileDialog.getExistingDirectory(self,caption="Set Datalog Folder",directory = MainWidget.workingDir)
        if path!="":
            self.datalogFolderPath = path
            self.datalogFolderWidgets["textEdit"].setText(path)
    
    def copyLayoutSetActive(self,state):
        for key in self.datalogFolderWidgets.keys():
            self.datalogFolderWidgets[key].setEnabled(state)#Enable/Disable the widgets

    def export(self):
        if (self.currentRecipeName != ''):
            extension = self.currentRecipeName.split('.')[-1]
            name = self.currentRecipeName[:-(len(extension)+1)]
            xsi="{http://www.w3.org/2001/XMLSchema-instance}"
            steps = self.editor.GetCurrentList()
            root = ET.Element('CParam_Recipe')
            tree = ET.ElementTree(root)
            
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
                        
            tree.write(self.currentRecipePath+self.currentRecipeName, encoding="utf-8", xml_declaration=True) 
            self.editor.ChangeTitleofTab(name)
            self.messageChanged.emit("Recipe exported to {}".format(self.currentRecipeName))
        else:
            self.messageChanged.emit("Failed to export, filename empty")
        if self.copyCheckBox.isChecked():
            #Copy the recipe to the datalog folder
            #Tries to create it if it does'nt exist already
            os.makedirs(self.datalogFolderPath, exist_ok=True)
            shutil.copy2(self.currentRecipePath+self.currentRecipeName,self.datalogFolderPath+'/'+self.currentRecipeName)
        self.accept()