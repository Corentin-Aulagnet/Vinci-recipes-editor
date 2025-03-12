from mainwidget import MainWidget
from PyQt5.QtWidgets import QApplication,QListView,QDialog,QVBoxLayout,QHBoxLayout,QLabel,QStyle,QPushButton,QLineEdit,QFileDialog,QCheckBox 
from PyQt5.QtCore import Qt,QStringListModel
from PyQt5.QtGui import QIcon
class ManageUsersWindow(MainWidget,QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.currentUserChanged.connect(self.changeCurrentUserText)
        #Current user label
        self.currentUserLabel = QLabel(f"Current user: {MainWidget.currentUser}")
        #StringListView
        self.model = QStringListModel()
        self.model.setStringList(MainWidget.GetRegisteredUsers())
        self.listView = QListView()
        self.listView.setSelectionMode(QListView.SingleSelection)
        self.listView.setModel(self.model)
        #Buttons
        self.addButton = QPushButton("+")
        self.addButton.clicked.connect(self.onAddUser)
        self.removeButton = QPushButton("-")
        self.removeButton.clicked.connect(self.onRemoveUser)
        self.selectButton = QPushButton("Select")
        self.selectButton.clicked.connect(self.onSelectUser)
        #layout
        self.mainLayout = QVBoxLayout()
        self.listLayout = QHBoxLayout()
        self.listButtonsLayout = QVBoxLayout()

        self.listLayout.addWidget(self.listView)
        self.listButtonsLayout.addWidget(self.addButton)
        self.listButtonsLayout.addWidget(self.removeButton)
        self.listLayout.addLayout(self.listButtonsLayout)

        self.mainLayout.addWidget(self.currentUserLabel)
        self.mainLayout.addLayout(self.listLayout)
        self.mainLayout.addWidget(self.selectButton)
        
        

        self.setLayout(self.mainLayout)
        self.show()

    def onAddUser(self):
        class AddUserDialog(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle("Add User")
                self.layout = QVBoxLayout()

                self.label = QLabel("Enter user name:")
                self.layout.addWidget(self.label)

                self.lineEdit = QLineEdit()
                self.layout.addWidget(self.lineEdit)

                #Adds an horizontal layout for the recipe file
                self.workingDirLayout = QHBoxLayout()
                self.datalogFolderWidgets={"textEdit":None,"button":None}
                
                textInput = QLineEdit()
                textInput.setReadOnly(True)
                self.datalogFolderWidgets["textEdit"] = textInput
                button = QPushButton(icon=QApplication.style().standardIcon(QStyle.SP_DirIcon))
                button.clicked.connect(self.OpenFolderPathWindow)
                self.datalogFolderWidgets["button"] = button

                for key in self.datalogFolderWidgets.keys():
                    self.workingDirLayout.addWidget(self.datalogFolderWidgets[key])
                self.layout.addWidget(QLabel("Choose working directory:"))
                self.layout.addLayout(self.workingDirLayout)
                self.buttons = QHBoxLayout()
                self.okButton = QPushButton("OK")
                self.okButton.clicked.connect(self.accept)
                self.cancelButton = QPushButton("Cancel")
                self.cancelButton.clicked.connect(self.reject)
                self.buttons.addWidget(self.okButton)
                self.buttons.addWidget(self.cancelButton)

                self.layout.addLayout(self.buttons)
                self.setLayout(self.layout)
            def OpenFolderPathWindow(self):
                path = QFileDialog.getExistingDirectory(self,caption="Choose Working Directory",directory = self.WORKING_DIR)
                if path!="":
                    self.datalogFolderWidgets["textEdit"].setText(path)
            def getUserName(self):
                return self.lineEdit.text()
            def getWorkingDir(self):
                return self.datalogFolderWidgets["textEdit"].text()
        dialog = AddUserDialog(self)
        if dialog.exec() == QDialog.Accepted:
            userName = dialog.getUserName()
            workingDir = dialog.getWorkingDir()
            if userName and (not userName in MainWidget.getRegisteredUsers()):
                #userName is not null and not yet registered
                MainWidget.userPrefs[userName] = {MainWidget.WORKING_DIR_VAR : workingDir}  
                self.currentUserLabel.setText(f"Current user: {MainWidget.currentUser}")
                self.model.setStringList(MainWidget.getRegisteredUsers())
                MainWidget.activateUser(userName)
    def onRemoveUser(self):
        user = self.listView.selectedIndexes()[0].data()
        del MainWidget.userPrefs[user]
        self.model.setStringList(MainWidget.getRegisteredUsers())
        if user == MainWidget.currentUser:
            MainWidget.activateUser(MainWidget.getRegisteredUsers()[0])
            
    def changeCurrentUserText(self,userName):
        self.currentUserLabel.setText(f"Current user: {MainWidget.currentUser}")
    def onSelectUser(self):
        #Get the user selected in the listView
        user = self.listView.selectedIndexes()[0].data()
        MainWidget.activateUser(user)
        self.currentUserChanged.emit(user)
        #self.currentUserLabel.setText(f"Current user: {MainWidget.currentUser}")

