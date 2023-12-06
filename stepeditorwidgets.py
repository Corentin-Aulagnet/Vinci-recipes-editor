from PyQt5.QtWidgets import QLineEdit,QComboBox,QWidget,QListWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel,QDialog
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt,QAbstractListModel,QModelIndex,QRect
from vincirecipereader import Step,Recipe

def clearLayout(layout):
    if layout != None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                clearLayout(child)

class BaseStepEditor(QDialog):
    def __init__(self,step,parent=None):
        super().__init__(parent)
        self.step = step
        self.setWindowTitle(step.type)
        self.layout = QVBoxLayout()
        self.setGeometry(QRect(100, 100, 400, 200))
        self.formLayout=QGridLayout()
        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.close)
        self.layout.addLayout(self.formLayout)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)

    def close(self):
        #Communicate Step back to parent
        #Close widget
        self.done(1)




class MassflowSetpoint(BaseStepEditor):
        def __init__(self,step,parent=None):
              super().__init__(step,parent)
              self.combo = QComboBox()
              self.combo.addItems(["Massflow 1","Massflow 2","Massflow 3"])

              match step.attr['Massflow_ID']:
                    case 'MASSFLOW_1':
                        self.combo.setCurrentIndex(0)
                    case 'MASSFLOW_2':
                        self.combo.setCurrentIndex(1)
                    case 'MASSFLOW_3':
                        self.combo.setCurrentIndex(2)

              self.formLayout.addWidget(QLabel("Massflow name"),0,0)
              self.formLayout.addWidget(self.combo,0,1)

              self.edit = QLineEdit()
              self.edit.setText(step.attr['SetPoint_sccm'])
              self.formLayout.addWidget(QLabel("Setpoint"),1,0)
              self.formLayout.addWidget(self.edit,1,1)

        def close(self):
            match self.combo.currentIndex():
                    case 0:
                        self.step.attr['Massflow_ID'] = 'MASSFLOW_1'
                    case 1:
                        self.step.attr['Massflow_ID'] = 'MASSFLOW_2'
                    case 2:
                        self.step.attr['Massflow_ID'] = 'MASSFLOW_3'
            self.step.attr['SetPoint_sccm'] = self.edit.text()
            super().close()

class VATValve(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.setpointLayout = QHBoxLayout(self)
                self.combo.addItems(["Closed","Open","Position control",'Pressure control'])
                self.combo.currentIndexChanged.connect(self.redrawform)
                match step.attr['Mode']:
                    case 'Closed':
                        self.combo.setCurrentIndex(0)
                    case 'Open':
                        self.combo.setCurrentIndex(1)
                    case 'PositionControl':
                        self.combo.setCurrentIndex(2)
                    case 'PressureControl':
                        self.combo.setCurrentIndex(3)

                self.formLayout.addWidget(QLabel("Mode"),0,0)
                self.formLayout.addWidget(self.combo,0,1)

               
                self.redrawform(self.combo.currentIndex())
                self.formLayout.addLayout(self.setpointLayout,1,0,1,-1)
                
        
        @pyqtSlot(int)
        def redrawform(self,index):
            clearLayout(self.setpointLayout)
            self.edit = QLineEdit()
            self.edit.setText(self.step.attr['Setpoint'])
            self.setpointLayout.addWidget(QLabel("Setpoint"))
            self.setpointLayout.addStretch()
            self.setpointLayout.addWidget(self.edit)
            match index:
                case 2:
                    self.setpointLayout.addWidget(QLabel("%"))
                case 3:
                    self.setpointLayout.addWidget(QLabel("mBar"))

        def close(self):
            match self.combo.currentIndex():
                    case 0:
                        self.step.attr['Mode'] = 'Closed'
                    case 1:
                        self.step.attr['Mode'] = 'Open'
                    case 2:
                        self.step.attr['Mode'] = 'PositionControl'
                    case 3:
                        self.step.attr['Mode'] = 'PressureControl'
            
            self.step.attr['Setpoint'] = self.edit.text()
            super().close()