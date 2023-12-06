from PyQt5.QtWidgets import QLineEdit,QComboBox,QWidget,QListWidget,QVBoxLayout,QGridLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel,QDialog
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt,QAbstractListModel,QModelIndex,QRect
from vincirecipereader import Step,Recipe

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
        match self.combo.currentIndex():
                    case 0:
                        self.step.attr['Massflow_ID'] = 'MASSFLOW_1'
                    case 1:
                        self.step.attr['Massflow_ID'] = 'MASSFLOW_2'
                    case 2:
                        self.step.attr['Massflow_ID'] = 'MASSFLOW_3'
        self.step.attr['SetPoint_sccm'] = self.edit.text()
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