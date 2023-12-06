from PyQt5.QtWidgets import QRadioButton,QButtonGroup,QLineEdit,QComboBox,QWidget,QListWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel,QDialog
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

class MaximPowerOff(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.combo.addItems(["Maxim 1","Maxim 2","Maxim 3"])

                match step.attr['Maxim_ID']:
                    case 'MAXIM_1':
                        self.combo.setCurrentIndex(0)
                    case 'MAXIM_2':
                        self.combo.setCurrentIndex(1)
                    case 'MAXIM_3':
                        self.combo.setCurrentIndex(2)

                self.formLayout.addWidget(QLabel("Maxim name"),0,0)
                self.formLayout.addWidget(self.combo,0,1)

                self.buttonGroup = QButtonGroup()
                self.offRadio = QRadioButton('Off')
                self.onRadio = QRadioButton('On')
                self.buttonGroup.addButton(self.onRadio)
                self.buttonGroup.addButton(self.offRadio)
                match self.step.attr['IsOn']:
                    case 'true':
                        self.onRadio.setChecked(True)
                    case 'false':
                        self.offRadio.setChecked(True)
                self.formLayout.addWidget(QLabel("State"),1,0)
                self.formLayout.addWidget(self.onRadio,1,1)
                self.formLayout.addWidget(self.offRadio,1,2)

        def close(self):
            match self.combo.currentIndex():
                    case 0:
                        self.step.attr['Maxim_ID'] = 'MAXIM_1'
                    case 1:
                        self.step.attr['Maxim_ID'] = 'MAXIM_2'
                    case 2:
                        self.step.attr['Maxim_ID'] = 'MAXIM_3'
            if self.onRadio.isChecked() : self.step.attr['IsOn'] = 'true' 
            else: self.step.attr['IsOn'] = 'false'
            super().close()

class MaximSetpoints(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.combo.addItems(["Maxim 1","Maxim 2","Maxim 3"])

                match step.attr['Maxim_ID']:
                    case 'MAXIM_1':
                        self.combo.setCurrentIndex(0)
                    case 'MAXIM_2':
                        self.combo.setCurrentIndex(1)
                    case 'MAXIM_3':
                        self.combo.setCurrentIndex(2)

                self.formLayout.addWidget(QLabel("Maxim name"),0,0)
                self.formLayout.addWidget(self.combo,0,1)

                self.powerEdit = QLineEdit()
                self.powerEdit.setText(step.attr['Power'])
                self.formLayout.addWidget(QLabel("Power setpoint"),1,0)
                self.formLayout.addWidget(self.powerEdit,1,1)
                self.formLayout.addWidget(QLabel("Watts"),1,2)

                self.currentEdit = QLineEdit()
                self.currentEdit.setText(step.attr['Current'])
                self.formLayout.addWidget(QLabel("Current setpoint"),2,0)
                self.formLayout.addWidget(self.currentEdit,2,1)
                self.formLayout.addWidget(QLabel("Amps"),2,2)

                self.voltageEdit = QLineEdit()
                self.voltageEdit.setText(step.attr['Voltage'])
                self.formLayout.addWidget(QLabel("Voltage setpoint"),3,0)
                self.formLayout.addWidget(self.voltageEdit,3,1)
                self.formLayout.addWidget(QLabel("Volts"),3,2)

                self.rampTimeEdit = QLineEdit()
                self.rampTimeEdit.setText(step.attr['RampTime'])
                self.formLayout.addWidget(QLabel("RampTime setpoint"),4,0)
                self.formLayout.addWidget(self.rampTimeEdit,4,1)
                self.formLayout.addWidget(QLabel("s"),4,2)

                self.arcDetectEdit = QLineEdit()
                self.arcDetectEdit.setText(step.attr['ArcDetectDelayTime'])
                self.formLayout.addWidget(QLabel("Arc detect delay time setpoint"),5,0)
                self.formLayout.addWidget(self.arcDetectEdit,5,1)
                self.formLayout.addWidget(QLabel("µs"),5,2)

                self.arcOffEdit = QLineEdit()
                self.arcOffEdit.setText(step.attr['ArcOffTime'])
                self.formLayout.addWidget(QLabel("Arc off time setpoint"),6,0)
                self.formLayout.addWidget(self.arcOffEdit,6,1)
                self.formLayout.addWidget(QLabel("µs"),6,2)

        def close(self):
            match self.combo.currentIndex():
                    case 0:
                        self.step.attr['Maxim_ID'] = 'MAXIM_1'
                    case 1:
                        self.step.attr['Maxim_ID'] = 'MAXIM_2'
                    case 2:
                        self.step.attr['Maxim_ID'] = 'MAXIM_3'
            self.step.attr['Power'] = self.powerEdit.text()
            self.step.attr['Current'] = self.currentEdit.text()
            self.step.attr['Voltage'] = self.voltageEdit.text()
            self.step.attr['RampTime'] = self.rampTimeEdit.text()
            self.step.attr['ArcDetectDelayTime'] = self.arcDetectEdit.text()
            self.step.attr['ArcOffTime'] = self.arcOffEdit.text()
            super().close()