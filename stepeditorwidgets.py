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
              self.combo.addItems(["Massflow #1 Argon","Massflow #2 Oxygen","Massflow #3 Nitrogen"])

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


class Sleep(BaseStepEditor):
        def __init__(self,step,parent=None):
              super().__init__(step,parent)

              self.edit = QLineEdit()
              self.edit.setText(step.attr['WaitTime_Sec'])
              self.formLayout.addWidget(QLabel("Wait time"),1,0)
              self.formLayout.addWidget(self.edit,1,1)
              self.formLayout.addWidget(QLabel("s"),1,2)

        def close(self):
            self.step.attr['WaitTime_Sec'] = self.edit.text()
            super().close()

class SubstrateHeating(BaseStepEditor):
        def __init__(self,step,parent=None):
              super().__init__(step,parent)

              self.edit = QLineEdit()
              self.edit.setText(step.attr['SetPoint_Deg'])
              self.formLayout.addWidget(QLabel("Temperature setpoint"),1,0)
              self.formLayout.addWidget(self.edit,1,1)
              self.formLayout.addWidget(QLabel("°C"),1,2)

        def close(self):
            self.step.attr['SetPoint_Deg'] = self.edit.text()
            super().close()

class PowerSwitcher(BaseStepEditor):
        switcher_supply = {
             'Power switcher 1':['Seren 2','Maxim 1'],
             'Power switcher 2':['Maxim 2','Maxim 3']

        }
        supply_cathodes= {
             'SEREN 2' : ['None','Cathode 1','Cathode 2','Cathode 3','Cathode 4'],
             'Maxim 1' : ['None','Cathode 1','Cathode 2','Cathode 3','Cathode 4'],
             'Maxim 2' : ['None','Cathode 5','Cathode 6','Cathode 7','Cathode 8'],
             'Maxim 3' : ['None','Cathode 5','Cathode 6','Cathode 7','Cathode 8']         
            }
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.switcherCombo = QComboBox()
                self.switcherCombo.addItems(PowerSwitcher.switcher_supply.keys())

                match step.attr['PowerSwitcher_ID']:
                    case 'SWITCHER_1':
                        self.switcherCombo.setCurrentIndex(0)
                    case 'SWITCHER_2':
                        self.switcherCombo.setCurrentIndex(1)
                self.switcherCombo.currentIndexChanged.connect(self.redrawSupplyLayout)
                self.formLayout.addWidget(QLabel("Power switcher"),0,0)
                self.formLayout.addWidget(self.switcherCombo,0,1)


                self.supplyLayout = QHBoxLayout()
                self.supplyCombo = QComboBox()
                self.supplyLayout.addWidget(QLabel("Power supply"))
                self.supplyLayout.addWidget(self.supplyCombo)
                self.formLayout.addLayout(self.supplyLayout,1,0,1,-1)
                self.redrawSupplyLayout(self.switcherCombo.currentIndex())

                self.cathodesLayout = QHBoxLayout()
                self.cathodesCombo = QComboBox()
                self.cathodesLayout.addWidget(QLabel("Cathode"))
                self.cathodesLayout.addWidget(self.cathodesCombo)
                self.formLayout.addLayout(self.cathodesLayout,2,0,1,-1)
                self.redrawCathodesLayout(self.supplyCombo.currentIndex())

                

        @pyqtSlot(int)
        def redrawSupplyLayout(self,index):
            self.supplyCombo.clear()
            match index:
                case 0:
                      self.supplyCombo.addItems(self.switcher_supply['Power switcher 1'])
                case 1:
                      self.supplyCombo.addItems(self.switcher_supply['Power switcher 2'])
            
            match self.step.attr['PowerSwitcher_InputID']:
                    case 'IN_1':
                        self.supplyCombo.setCurrentIndex(0)
                    case 'IN_2':
                        self.supplyCombo.setCurrentIndex(1)

            self.supplyCombo.currentIndexChanged.connect(self.redrawCathodesLayout)
            

        @pyqtSlot(int)
        def redrawCathodesLayout(self,index):
            self.cathodesCombo.clear()
            match self.supplyCombo.itemText(index):
                case 'SEREN 2':
                      self.cathodesCombo.addItems(self.supply_cathodes['SEREN 2'])
                case 'Maxim 1':
                      self.cathodesCombo.addItems(self.supply_cathodes['Maxim 1'])
                case 'Maxim 2':
                      self.cathodesCombo.addItems(self.supply_cathodes['Maxim 2'])
                case 'Maxim 3':
                      self.cathodesCombo.addItems(self.supply_cathodes['Maxim 3'])

            
            match self.step.attr['PowerSwitcher_OutputID']:
                    case 'NONE':
                        self.cathodesCombo.setCurrentIndex(0)
                    case 'OUT_1':
                        self.cathodesCombo.setCurrentIndex(1)
                    case 'OUT_2':
                        self.cathodesCombo.setCurrentIndex(2)
                    case 'OUT_3':
                        self.cathodesCombo.setCurrentIndex(3)
                    case 'OUT_4':
                        self.cathodesCombo.setCurrentIndex(4)
            
        def close(self):
            if self.switcherCombo.currentIndex() == 0:
                #Switcher 1 is selected
                self.step.attr["Command_VariableID"] = 'MW_SW1_DC_COMMAND' 
                self.step.attr["State_VariableID"] = 'MW_SW1_DC_STATE'
                self.step.attr["PowerSwitcher_ID"] = 'SWITCHER_1'
            else:
                #Switcher 2 is selected
                self.step.attr["Command_VariableID"] = 'MW_SW2_DC_COMMAND' 
                self.step.attr["State_VariableID"] = 'MW_SW2_DC_STATE'
                self.step.attr["PowerSwitcher_ID"] = 'SWITCHER_2'
            match self.supplyCombo.currentIndex():
                case 1:
                    #IN_1
                    self.step.attr["PowerSwitcher_InputID"] = 'IN_1'
                case 2:
                    #IN_2
                    self.step.attr["PowerSwitcher_InputID"] = 'IN_2'
            match self.cathodesCombo.currentIndex():
                case 0:
                    #None
                    self.step.attr["PowerSwitcher_OutputID"] = 'NONE'
                case 1:
                    #OUT_1
                    self.step.attr["PowerSwitcher_OutputID"] = 'OUT_1'
                case 2:
                    #OUT_2
                    self.step.attr["PowerSwitcher_OutputID"] = 'OUT_2'
                case 3:
                    #OUT_3
                    self.step.attr["PowerSwitcher_OutputID"] = 'OUT_3'
                case 4:
                    #OUT_4
                    self.step.attr["PowerSwitcher_OutputID"] = 'OUT_4'
            super().close()

class ShutterOpenClose(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.combo.addItems(["Cathode {}".format(i) for i in range(1,9)])

                match step.attr['Command_VariableID']:
                    case 'MX_DC_Shutter1_COMMAND':
                        self.combo.setCurrentIndex(0)
                    case 'MX_DC_Shutter2_COMMAND':
                        self.combo.setCurrentIndex(1)
                    case 'MX_DC_Shutter3_COMMAND':
                        self.combo.setCurrentIndex(2)
                    case 'MX_DC_Shutter4_COMMAND':
                        self.combo.setCurrentIndex(3)
                    case 'MX_DC_Shutter5_COMMAND':
                        self.combo.setCurrentIndex(4)
                    case 'MX_DC_Shutter6_COMMAND':
                        self.combo.setCurrentIndex(5)
                    case 'MX_DC_Shutter7_COMMAND':
                        self.combo.setCurrentIndex(6)
                    case 'MX_DC_Shutter8_COMMAND':
                        self.combo.setCurrentIndex(7)

                self.formLayout.addWidget(QLabel("Shutter name"),0,0)
                self.formLayout.addWidget(self.combo,0,1)

                self.buttonGroup = QButtonGroup()
                self.offRadio = QRadioButton('Closed')
                self.onRadio = QRadioButton('Open')
                self.buttonGroup.addButton(self.onRadio)
                self.buttonGroup.addButton(self.offRadio)
                match self.step.attr['OpenState']:
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
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter1_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter1_STATE'
                    case 1:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter2_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter2_STATE'
                    case 2:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter3_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter3_STATE'
                    case 3:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter4_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter4_STATE'
                    case 4:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter5_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter5_STATE'
                    case 5:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter6_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter6_STATE'
                    case 6:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter7_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter7_STATE'
                    case 7:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter8_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter8_STATE'
            if self.onRadio.isChecked() : self.step.attr['OpenState'] = 'true' 
            else: self.step.attr['OpenState'] = 'false'
            super().close()


class ValveOpenClose(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.combo.addItems(["Deposit chamber Backing valve",
                                     "Deposit chamber Gas injection valve",
                                     "Deposit chamber Roughing valve",
                                     "Deposit chamber Venting valve",
                                     "Loadlock chamber Backing valve",
                                     "Loadlock chamber Venting valve",
                                     "Massflow #1 Gas injection valve",
                                     "Massflow #2 Gas injection valve",
                                     "Massflow #3 Gas injection valve"])

                match step.attr['Command_VariableID']:
                    case 'MX_DC_BackingValve_COMMAND':
                        self.combo.setCurrentIndex(0)
                    case 'MX_DC_GasInjectionValve_COMMAND':
                        self.combo.setCurrentIndex(1)
                    case 'MX_DC_RoughingValve_COMMAND':
                        self.combo.setCurrentIndex(2)
                    case 'MX_DC_VentingValve_COMMAND':
                        self.combo.setCurrentIndex(3)
                    case 'MX_LL_BackingValve_COMMAND':
                        self.combo.setCurrentIndex(4)
                    case 'MX_LL_VentingValve_COMMAND':
                        self.combo.setCurrentIndex(5)
                    case 'MX_DC_MF1_GasInjectionValve_COMMAND':
                        self.combo.setCurrentIndex(6)
                    case 'MX_DC_MF2_GasInjectionValve_COMMAND':
                        self.combo.setCurrentIndex(7)
                    case 'MX_DC_MF3_GasInjectionValve_COMMAND':
                        self.combo.setCurrentIndex(8)

                self.formLayout.addWidget(QLabel("Valve name"),0,0)
                self.formLayout.addWidget(self.combo,0,1)

                self.buttonGroup = QButtonGroup()
                self.offRadio = QRadioButton('Closed')
                self.onRadio = QRadioButton('Open')
                self.buttonGroup.addButton(self.onRadio)
                self.buttonGroup.addButton(self.offRadio)
                match self.step.attr['OpenState']:
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
                        self.step.attr['Command_VariableID'] = 'MX_DC_BackingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_BackingValve_STATE'
                    case 1:
                        self.step.attr['Command_VariableID'] = 'MX_DC_GasInjectionValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_GasInjectionValve_STATE'
                    case 2:
                        self.step.attr['Command_VariableID'] = 'MX_DC_RoughingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_RoughingValve_STATE'
                    case 3:
                        self.step.attr['Command_VariableID'] = 'MX_DC_VentingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_VentingValve_STATE'
                    case 4:
                        self.step.attr['Command_VariableID'] = 'MX_LL_BackingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_LL_BackingValve_STATE'
                    case 5:
                        self.step.attr['Command_VariableID'] = 'MX_LL_VentingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_LL_VentingValve_STATE'
                    case 6:
                        self.step.attr['Command_VariableID'] = 'MX_DC_MF1_GasInjectionValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_MF1_GasInjectionValve_STATE'
                    case 7:
                        self.step.attr['Command_VariableID'] = 'MX_DC_MF2_GasInjectionValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_MF2_GasInjectionValve_STATE'
                    case 8:
                        self.step.attr['Command_VariableID'] = 'MX_DC_MF3_GasInjectionValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_MF3_GasInjectionValve_STATE'
            if self.onRadio.isChecked() : self.step.attr['OpenState'] = 'true' 
            else: self.step.attr['OpenState'] = 'false'
            super().close()