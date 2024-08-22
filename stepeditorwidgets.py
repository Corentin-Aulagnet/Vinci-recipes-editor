from PyQt5.QtWidgets import QLayout,QRadioButton,QButtonGroup,QLineEdit,QComboBox,QWidget,QListWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel,QDialog
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
def clearWidget(widget):
    children = widget.findChildren(QWidget)
    for child in children:
        child.deleteLater()
    children = widget.findChildren(QLayout)
    for child in children:        
        clearLayout(child)

class StepAddPopUp(QDialog):
    def __init__(self,step,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add a new step")
        self.setGeometry(QRect(100, 100, 400, 200))
        self.layout = QGridLayout()
        self.okButton = QPushButton("Ok")
        self.combo = QComboBox()
        self.step = step
        self.step_display_names=["Massflow Setpoint",
                             "Vat Valve",
                             "Maxim Power Off",
                             "Maxim Setpoints",
                             "Seren MC2",
                             "Seren Rx01",
                             "PowerSwitcher",
                             "Sleep",
                             "Substrate Heating Off",
                             "Substrate Heating On",
                             "Substrate Rotation Off",
                             "Substrate Rotation On",
                             "Substrate Heating Setpoint",
                             "Shutter Open Close",
                             "Valve Open Close"]
        self.combo.addItems(self.step_display_names)
        self.combo.currentIndexChanged.connect(self.redrawForm)
        self.okButton.clicked.connect(self.close)
        self.editorLayout = QVBoxLayout()
        self.editorWidget = QWidget()
        self.editorLayout.addWidget(self.editorWidget)
        self.redrawForm(0)
        
        self.layout.addWidget(QLabel("Step type"),0,0)
        self.layout.addWidget(self.combo,0,1)
        self.layout.addLayout(self.editorLayout,1,0,1,-1)
        self.layout.addWidget(self.okButton,2,0,1,-1)
        self.setLayout(self.layout)
    @pyqtSlot(int)
    def redrawForm(self,index):
        self.step.clear()
        clearLayout(self.editorLayout)
        if self.combo.itemText(index) == self.step_display_names[0]:
            self.step.type = "CParamScript_MassflowSetpoint"
            self.step.Add_attr("Massflow_ID",'0')
            self.step.Add_attr("Measure_VariableID",'0')
            self.step.Add_attr("Setpoint_VariableID",'0')
            self.step.Add_attr("SetPoint_sccm",'0')
            self.editorWidget = MassflowSetpoint(self.step,self)

        elif self.combo.itemText(index) == self.step_display_names[1]:
            self.step.type = "CParamScript_VatValve"
            self.step.Add_attr("Mode",'0')
            self.step.Add_attr("Setpoint",'0')
            self.editorWidget = VATValve(self.step,self)

        elif self.combo.itemText(index) ==  self.step_display_names[2]:
            self.step.type = "CParamScript_Maxim_PowerOff"
            self.step.Add_attr("Maxim_ID",'0')
            self.step.Add_attr("IsOn",'0')
            self.editorWidget = MaximPowerOff(self.step,self)

        elif self.combo.itemText(index) ==  self.step_display_names[3]:
            self.step.type = "CParamScript_Maxim_Setpoints"
            self.step.Add_attr("Maxim_ID",'0')
            self.step.Add_attr("Power",'0')
            self.step.Add_attr("Current",'0')
            self.step.Add_attr("Voltage",'0')
            self.step.Add_attr("RampTime",'0')
            self.step.Add_attr("ArcDetectDelayTime",'0')
            self.step.Add_attr("ArcOffTime",'0')
            self.editorWidget = MaximSetpoints(self.step,self)

        elif self.combo.itemText(index) ==  self.step_display_names[4]:
            self.step.type = "CParamScript_Seren_MC2_Setpoints"
            self.step.Add_attr("SerenID",'0')
            self.step.Add_attr("TuneCapacitor",'0')
            self.step.Add_attr("LoadCapacitor",'0')
            self.step.Add_attr("TuneCapacitor_Setpoint_VariableID",'0')
            self.step.Add_attr("LoadCapacitor_Setpoint_VariableID",'0')
            self.step.Add_attr("TuneCapacitor_SetCommand_VariableID",'0')
            self.step.Add_attr("LoadCapacitor_SetCommand_VariableID",'0')
            self.editorWidget = SerenMC2(self.step,self)

        elif self.combo.itemText(index) ==  self.step_display_names[5]:
            self.step.type = "CParamScript_Seren_Rx01_Setpoints"
            self.step.Add_attr("SerenID",'0')
            self.step.Add_attr("Mode",'0')
            self.step.Add_attr("Setpoint",'0')
            self.step.Add_attr("Synchronisation",'0')
            self.step.Add_attr("ContinuousPulse",'0')
            self.step.Add_attr("PulseTrain",'0')
            self.step.Add_attr("Mode_Command_VariableID",'0')
            self.step.Add_attr("Mode_State_VariableID",'0')
            self.step.Add_attr("OutputSetpoint_VariableID",'0')
            self.step.Add_attr("Synchronisation_Command_VariableID",'0')
            self.step.Add_attr("Synchronisation_State_VariableID",'0')
            self.step.Add_attr("Output_Command_VariableID",'0')
            self.step.Add_attr("Output_State_VariableID",'0')
            self.step.Add_attr("ContinuousPulse_Command_VariableID",'0')
            self.step.Add_attr("ContinuousPulse_State_VariableID",'0')
            self.step.Add_attr("PulseTrain_Command_VariableID",'0')
            self.step.Add_attr("PulseTrain_State_VariableID",'0')
            self.editorWidget = SerenRx01(self.step,self)

        elif self.combo.itemText(index) ==  self.step_display_names[6]:
            self.step.type = "CParamScript_PowerSwitcher"
            self.step.Add_attr("DeviceID","WAGO")
            self.step.Add_attr("Command_VariableID",'0')
            self.step.Add_attr("State_VariableID",'0')
            self.step.Add_attr("PowerSwitcher_ID",'0')
            self.step.Add_attr("PowerSwitcher_InputID",'0')
            self.step.Add_attr("PowerSwitcher_OutputID",'0')
            self.editorWidget = PowerSwitcher(self.step,self)

        elif self.combo.itemText(index) ==  self.step_display_names[7]:
            self.step.type = "CParamScript_Sleep"
            self.step.Add_attr("WaitTime_Sec",'0')
            self.editorWidget = Sleep(self.step,self)
                
        elif self.combo.itemText(index) ==  self.step_display_names[8]:
            self.step.type = "CParamScript_Substrate_HeatingOff"
            self.editorWidget = QWidget()

        elif self.combo.itemText(index) ==  self.step_display_names[9]:
            self.step.type = "CParamScript_Substrate_HeatingOn"
            self.editorWidget = QWidget()

        elif self.combo.itemText(index) ==  self.step_display_names[10]:
            self.step.type = "CParamScript_Substrate_RotationOff"
            self.editorWidget = QWidget()

        elif self.combo.itemText(index) ==  self.step_display_names[11]:
            self.step.type = "CParamScript_Substrate_RotationOn"
            self.editorWidget = QWidget()

        elif self.combo.itemText(index) ==  self.step_display_names[12]:
            self.step.type = "CParamScript_Substrate_HeatingSetpoint"
            self.step.Add_attr("SetPoint_Deg",'0')
            self.editorWidget = SubstrateHeating(self.step,self)

        elif self.combo.itemText(index) ==  self.step_display_names[13]:
            self.step.type = "CParamScript_Shutter_OpenClose"
            self.step.Add_attr("DeviceID","WAGO")
            self.step.Add_attr("Command_VariableID",'0')
            self.step.Add_attr("State_VariableID",'0')
            self.step.Add_attr("OpenState",'0')
            self.editorWidget = ShutterOpenClose(self.step,self)

        elif self.combo.itemText(index) ==  self.step_display_names[14]:
            self.step.type = "CParamScript_Valve_OpenClose"
            self.step.Add_attr("DeviceID","WAGO")
            self.step.Add_attr("Command_VariableID",'0')
            self.step.Add_attr("State_VariableID",'0')
            self.step.Add_attr("OpenState",'0')
            self.editorWidget = ValveOpenClose(self.step,self)
        self.editorLayout.addWidget(self.editorWidget)
    
    def close(self):
        self.editorWidget.close()
        self.done(1)

class StepEditorPopUp(QDialog):
    def __init__(self,step,parent=None):
        super().__init__(parent)
        self.step = step
        self.setWindowTitle(step.type)
        self.setGeometry(QRect(100, 100, 400, 200))
        self.layout = QVBoxLayout()
        self.okButton = QPushButton("Ok")
        if step.type == "CParamScript_MassflowSetpoint":
            self.editorWidget = MassflowSetpoint(step,self)
        elif step.type == "CParamScript_VatValve":
            self.editorWidget = VATValve(step,self)
        elif step.type ==  "CParamScript_Maxim_PowerOff":
            self.editorWidget = MaximPowerOff(step,self)
        elif step.type ==  "CParamScript_Seren_MC2_Setpoints":
            self.editorWidget = SerenMC2(step,self)
        elif step.type ==  "CParamScript_Seren_Rx01_Setpoints":
            self.editorWidget = SerenRx01(step,self)
        elif step.type ==  "CParamScript_PowerSwitcher":
            self.editorWidget = PowerSwitcher(step,self)
        elif step.type ==  "CParamScript_Sleep":
            self.editorWidget = Sleep(step,self)
        elif step.type ==  "CParamScript_Substrate_HeatingSetpoint":
            self.editorWidget = SubstrateHeating(step,self)
        elif step.type ==  "CParamScript_Shutter_OpenClose":
            self.editorWidget = ShutterOpenClose(step,self)
        elif step.type ==  "CParamScript_Valve_OpenClose":
            self.editorWidget = ValveOpenClose(step,self)
        else: 
            self.isValid = False
            return
        self.okButton.clicked.connect(self.close)
        self.layout.addWidget(self.editorWidget)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)
        self.isValid = True
    def close(self):
        self.editorWidget.close()
        self.done(1)

class BaseStepEditor(QWidget):
    def __init__(self,step,parent=None):
        super().__init__(parent)
        self.step = step
        self.formLayout=QGridLayout()
        self.setLayout(self.formLayout)

    def close(self):
        pass


class SerenRx01(BaseStepEditor):
    def __init__(self,step,parent=None):
        super().__init__(step,parent)

        #Seren Selection
        self.combo = QComboBox()
        self.combo.addItems(["Seren #1", "Seren #2"])
        if step.attr['SerenID'] == 'SEREN_1':
            self.combo.setCurrentIndex(0)
        elif step.attr['SerenID'] == 'SEREN_2':
            self.combo.setCurrentIndex(1)
        self.formLayout.addWidget(QLabel("Seren name"),0,0)
        self.formLayout.addWidget(self.combo,0,1)

        #Mode
        self.modeGroup = QButtonGroup()
        self.powerRadio = QRadioButton('Power')
        self.voltageRadio = QRadioButton('Voltage')
        self.modeGroup.addButton(self.powerRadio)
        self.modeGroup.setId(self.powerRadio,0)
        self.modeGroup.addButton(self.voltageRadio)
        self.modeGroup.setId(self.voltageRadio,1)
        if self.step.attr['Mode'] == 'POWER':
                self.powerRadio.setChecked(True)
        elif self.step.attr['Mode'] == 'VOLTAGE':
                self.voltageRadio.setChecked(True)
        self.formLayout.addWidget(QLabel("Mode"),1,0)
        self.formLayout.addWidget(self.powerRadio,1,1)
        self.formLayout.addWidget(self.voltageRadio,1,2)
        self.modeGroup.idClicked.connect(self.redrawForm)



        #setpoint
        self.editSetpoint = QLineEdit()
        self.editSetpoint.setText(self.step.attr['Setpoint'])
        self.setpointLabel = QLabel("Setpoint")
        self.setpointUnitLabel = QLabel("W")
        self.formLayout.addWidget(self.setpointLabel,2,0)
        self.formLayout.addWidget(self.editSetpoint,2,1)
        self.formLayout.addWidget(self.setpointUnitLabel,2,2)
        

        #Synchronisation
        self.syncGroup = QButtonGroup()
        self.masterRadio = QRadioButton('Master')
        self.slaveRadio = QRadioButton('Slave')
        self.syncGroup.addButton(self.masterRadio)
        self.syncGroup.setId(self.masterRadio,0)
        self.syncGroup.addButton(self.slaveRadio)
        self.syncGroup.setId(self.slaveRadio,1)
        if self.step.attr['Synchronisation'] == 'MASTER':
                self.masterRadio.setChecked(True)
        elif self.step.attr['Synchronisation'] == 'SLAVE':
                self.slaveRadio.setChecked(True)
        self.formLayout.addWidget(QLabel("Synchronisation"),3,0)
        self.formLayout.addWidget(self.masterRadio,3,1)
        self.formLayout.addWidget(self.slaveRadio,3,2)

        #Output Mode
        self.outputGroup = QButtonGroup()
        self.contRadio = QRadioButton('Continuous')
        self.pulseRadio = QRadioButton('Pulse')
        self.outputGroup.addButton(self.contRadio)
        self.outputGroup.setId(self.contRadio,0)
        self.outputGroup.addButton(self.pulseRadio)
        self.outputGroup.setId(self.pulseRadio,1)
        if self.step.attr['ContinuousPulse'] == 'CONTINUOUS':
                self.contRadio.setChecked(True)
        elif self.step.attr['ContinuousPulse'] == 'PULSE':
                self.pulseRadio.setChecked(True)
        self.formLayout.addWidget(QLabel("Output Mode"),4,0)
        self.formLayout.addWidget(self.contRadio,4,1)
        self.formLayout.addWidget(self.pulseRadio,4,2)

        #Pulse train
        self.pulseTrainGroup = QButtonGroup()
        self.onRadio = QRadioButton('On')
        self.offRadio = QRadioButton('Off')
        self.pulseTrainGroup.addButton(self.onRadio)
        self.pulseTrainGroup.setId(self.onRadio,0)
        self.pulseTrainGroup.addButton(self.offRadio)
        self.pulseTrainGroup.setId(self.offRadio,1)
        if self.step.attr['PulseTrain'] == 'true':
                self.onRadio.setChecked(True)
        elif self.step.attr['PulseTrain'] == 'false':
                self.offRadio.setChecked(True)
        self.formLayout.addWidget(QLabel("Output Mode"),5,0)
        self.formLayout.addWidget(self.onRadio,5,1)
        self.formLayout.addWidget(self.offRadio,5,2)

    @pyqtSlot(int)
    def redrawForm(self,id):
        if id == 0:       
            #Power control mode
            self.setpointLabel.setText("Power Setpoint")
            self.setpointUnitLabel.setText("W")
        elif id == 1:
            #Voltage control mode
            self.setpointLabel.setText("Voltage Setpoint")
            self.setpointUnitLabel.setText("V")

    def close(self):
        #seren id
        if self.combo.currentIndex() == 0:
            self.step.attr['SerenID'] = "SEREN_1"
            self.step.attr["Mode_Command_VariableID"] = "MX_SEREN_Rx01_1_POWER_VOLTAGE_SW_COMMAND"
            self.step.attr["Mode_State_VariableID"] = "MX_SEREN_Rx01_1_POWER_VOLTAGE_SW_STATE"
            self.step.attr["OutputSetpoint_VariableID"] = "MDW_SEREN_Rx01_1_SP_Watts"
            self.step.attr["Synchronisation_Command_VariableID"] = "MX_SEREN_Rx01_1_EXCITATION_EXT_SW_COMMAND"
            self.step.attr["Synchronisation_State_VariableID"] = "MX_SEREN_Rx01_1_EXCITATION_EXT_SW_STATE"
            self.step.attr["Output_Command_VariableID"] = "MX_SEREN_Rx01_1_RF_OUTPUT_COMMAND"
            self.step.attr["Output_State_VariableID"]="MX_SEREN_Rx01_1_RF_OUTPUT_STATE"
            self.step.attr["ContinuousPulse_Command_VariableID"] = "MX_SEREN_Rx01_1_OUTPUT_TYPE_SW_COMMAND"
            self.step.attr["ContinuousPulse_State_VariableID"] = "MX_SEREN_Rx01_1_OUTPUT_TYPE_SW_STATE"
            self.step.attr["PulseTrain_Command_VariableID"] = "MX_SEREN_Rx01_1_PULSETRAIN_ONOFF_COMMAND"
            self.step.attr["PulseTrain_State_VariableID"] = "MX_SEREN_Rx01_1_PULSETRAIN_ONOFF_STATE"
        if self.combo.currentIndex() == 1:
            self.step.attr['SerenID'] = "SEREN_2"
            self.step.attr["Mode_Command_VariableID"] = "MX_SEREN_Rx01_2_POWER_VOLTAGE_SW_COMMAND"
            self.step.attr["Mode_State_VariableID"] = "MX_SEREN_Rx01_2_POWER_VOLTAGE_SW_STATE"
            self.step.attr["OutputSetpoint_VariableID"] = "MDW_SEREN_Rx01_2_SP_Watts"
            self.step.attr["Synchronisation_Command_VariableID"] = "MX_SEREN_Rx01_2_EXCITATION_EXT_SW_COMMAND"
            self.step.attr["Synchronisation_State_VariableID"] = "MX_SEREN_Rx01_2_EXCITATION_EXT_SW_STATE"
            self.step.attr["Output_Command_VariableID"] = "MX_SEREN_Rx01_2_RF_OUTPUT_COMMAND"
            self.step.attr["Output_State_VariableID"]="MX_SEREN_Rx01_2_RF_OUTPUT_STATE"
            self.step.attr["ContinuousPulse_Command_VariableID"] = "MX_SEREN_Rx01_2_OUTPUT_TYPE_SW_COMMAND"
            self.step.attr["ContinuousPulse_State_VariableID"] = "MX_SEREN_Rx01_2_OUTPUT_TYPE_SW_STATE"
            self.step.attr["PulseTrain_Command_VariableID"] = "MX_SEREN_Rx01_2_PULSETRAIN_ONOFF_COMMAND"
            self.step.attr["PulseTrain_State_VariableID"] = "MX_SEREN_Rx01_2_PULSETRAIN_ONOFF_STATE"

        #mode
        if self.powerRadio.isChecked():
            self.step.attr['Mode'] = 'POWER'
        else:
            self.step.attr['Mode'] = 'VOLTAGE'
        
        #setpoint
        self.step.attr['Setpoint'] = self.editSetpoint.text()

        #Synchronisation
        if self.masterRadio.isChecked():
            self.step.attr['Synchronisation'] = 'MASTER'
        else:
            self.step.attr['Synchronisation'] = 'SLAVE'

        #output mode
        if self.contRadio.isChecked():
            self.step.attr['ContinuousPulse'] = 'CONTINUOUS'
        else :
            self.step.attr['ContinuousPulse'] = 'PULSE'

        #pulseTrain
        if self.onRadio.isChecked(): 
            self.step.attr['PulseTrain'] = 'true'
        else:
            self.step.attr['PulseTrain'] = 'false'
            
        super().close()

class SerenMC2(BaseStepEditor):
    def __init__(self,step,parent=None):
        super().__init__(step,parent)
        #Seren Selection
        self.combo = QComboBox()
        self.combo.addItems(["Seren #1", "Seren #2"])
        if step.attr['SerenID'] == 'SEREN_1':
            self.combo.setCurrentIndex(0)
        elif step.attr['SerenID'] == 'SEREN_2':
            self.combo.setCurrentIndex(1)
        self.formLayout.addWidget(QLabel("Seren name"),0,0)
        self.formLayout.addWidget(self.combo,0,1)

        #Load capacity setpoint
        self.editLoad = QLineEdit()
        self.editLoad.setText(step.attr['LoadCapacitor'])
        self.formLayout.addWidget(QLabel("Load Capacity Setpoint"),1,0)
        self.formLayout.addWidget(self.editLoad,1,1)

         #Tune capacity setpoint
        self.editTune = QLineEdit()
        self.editTune.setText(step.attr['TuneCapacitor'])
        self.formLayout.addWidget(QLabel("Tune Capacity Setpoint"),2,0)
        self.formLayout.addWidget(self.editTune,2,1)

    def close(self):
        if self.combo.currentIndex() == 0:
            self.step.attr['SerenID'] = 'SEREN_1'
            self.step.attr['TuneCapacitor_Setpoint_VariableID'] = 'MDW_SEREN_MC2_1_TUNE_SETPOINT_Percent'
            self.step.attr['LoadCapacitor_Setpoint_VariableID'] = 'MDW_SEREN_MC2_1_LOAD_SETPOINT_Percent'
            self.step.attr['TuneCapacitor_SetCommand_VariableID'] = 'MX_SEREN_MC2_1_SET_TUNE_COMMAND'
            self.step.attr['LoadCapacitor_SetCommand_VariableID'] = 'MX_SEREN_MC2_1_SET_LOAD_COMMAND'

        elif self.combo.currentIndex() == 1:
            self.step.attr['SerenID'] = 'SEREN_2'
            self.step.attr['TuneCapacitor_Setpoint_VariableID'] = 'MDW_SEREN_MC2_2_TUNE_SETPOINT_Percent'
            self.step.attr['LoadCapacitor_Setpoint_VariableID'] = 'MDW_SEREN_MC2_2_LOAD_SETPOINT_Percent'
            self.step.attr['TuneCapacitor_SetCommand_VariableID'] = 'MX_SEREN_MC2_2_SET_TUNE_COMMAND'
            self.step.attr['LoadCapacitor_SetCommand_VariableID'] = 'MX_SEREN_MC2_2_SET_LOAD_COMMAND'

        self.step.attr['LoadCapacitor'] = self.editLoad.text()
        self.step.attr['TuneCapacitor'] = self.editTune.text()
        super().close()
class MassflowSetpoint(BaseStepEditor):
        def __init__(self,step,parent=None):
            super().__init__(step,parent)
            self.combo = QComboBox()
            self.combo.addItems(["Massflow #1 Argon","Massflow #2 Oxygen","Massflow #3 Nitrogen"])

            if step.attr['Massflow_ID'] == 'MASSFLOW_1':
                self.combo.setCurrentIndex(0)
            elif step.attr['Massflow_ID'] == 'MASSFLOW_2':
                self.combo.setCurrentIndex(1)
            elif step.attr['Massflow_ID'] == 'MASSFLOW_3':
                self.combo.setCurrentIndex(2)

            self.formLayout.addWidget(QLabel("Massflow name"),0,0)
            self.formLayout.addWidget(self.combo,0,1)

            self.edit = QLineEdit()
            self.edit.setText(step.attr['SetPoint_sccm'])
            self.formLayout.addWidget(QLabel("Setpoint"),1,0)
            self.formLayout.addWidget(self.edit,1,1)

        def close(self):
            if self.combo.currentIndex() == 0:
                self.step.attr['Massflow_ID'] = 'MASSFLOW_1'
                self.step.attr['Measure_VariableID'] = 'MDW_MF1_MES'
                self.step.attr['Setpoint_VariableID'] = 'MDW_MF1_SP'
            elif self.combo.currentIndex() == 1:
                self.step.attr['Massflow_ID'] = 'MASSFLOW_2'
                self.step.attr['Measure_VariableID'] = 'MDW_MF2_MES'
                self.step.attr['Setpoint_VariableID'] = 'MDW_MF2_SP'
            elif self.combo.currentIndex() == 2:
                self.step.attr['Massflow_ID'] = 'MASSFLOW_3'
                self.step.attr['Measure_VariableID'] = 'MDW_MF3_MES'
                self.step.attr['Setpoint_VariableID'] = 'MDW_MF3_SP'
            self.step.attr['SetPoint_sccm'] = self.edit.text()
            super().close()

class VATValve(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.setpointLayout = QHBoxLayout(self)
                self.combo.addItems(["Closed","Open","Position control",'Pressure control'])
                self.combo.currentIndexChanged.connect(self.redrawform)
                if step.attr['Mode'] == 'Closed':
                    self.combo.setCurrentIndex(0)
                elif step.attr['Mode'] == 'Open':
                        self.combo.setCurrentIndex(1)
                elif step.attr['Mode'] == 'PositionControl':
                        self.combo.setCurrentIndex(2)
                elif step.attr['Mode'] == 'PressureControl':
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
            if index == 2:
                self.setpointLayout.addWidget(QLabel("%"))
            elif index == 3:
                    self.setpointLayout.addWidget(QLabel("mBar"))

        def close(self):
            if self.combo.currentIndex() == 0:
                self.step.attr['Mode'] = 'Closed'
            elif self.combo.currentIndex() == 1:
                self.step.attr['Mode'] = 'Open'
            elif self.combo.currentIndex() == 2:
                self.step.attr['Mode'] = 'PositionControl'
            elif self.combo.currentIndex() == 3:
                self.step.attr['Mode'] = 'PressureControl'
            
            self.step.attr['Setpoint'] = self.edit.text()
            super().close()

class MaximPowerOff(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.combo.addItems(["Maxim 1","Maxim 2","Maxim 3"])

                if step.attr['Maxim_ID'] == 'MAXIM_1':
                    self.combo.setCurrentIndex(0)
                elif step.attr['Maxim_ID'] == 'MAXIM_2':
                    self.combo.setCurrentIndex(1)
                elif step.attr['Maxim_ID'] == 'MAXIM_3':
                    self.combo.setCurrentIndex(2)

                self.formLayout.addWidget(QLabel("Maxim name"),0,0)
                self.formLayout.addWidget(self.combo,0,1)

                self.buttonGroup = QButtonGroup()
                self.offRadio = QRadioButton('Off')
                self.onRadio = QRadioButton('On')
                self.buttonGroup.addButton(self.onRadio)
                self.buttonGroup.addButton(self.offRadio)
                if self.step.attr['IsOn'] == 'true':
                        self.onRadio.setChecked(True)
                elif self.step.attr['IsOn'] == 'false':
                        self.offRadio.setChecked(True)
                self.formLayout.addWidget(QLabel("State"),1,0)
                self.formLayout.addWidget(self.onRadio,1,1)
                self.formLayout.addWidget(self.offRadio,1,2)

        def close(self):
            if self.combo.currentIndex() == 0:
                self.step.attr['Maxim_ID'] = 'MAXIM_1'
            elif self.combo.currentIndex() == 1:
                self.step.attr['Maxim_ID'] = 'MAXIM_2'
            elif self.combo.currentIndex() == 2:
                self.step.attr['Maxim_ID'] = 'MAXIM_3'
            if self.onRadio.isChecked() : self.step.attr['IsOn'] = 'true' 
            else: self.step.attr['IsOn'] = 'false'
            super().close()

class MaximSetpoints(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.combo.addItems(["Maxim 1","Maxim 2","Maxim 3"])

                if step.attr['Maxim_ID'] == 'MAXIM_1':
                        self.combo.setCurrentIndex(0)
                elif step.attr['Maxim_ID'] == 'MAXIM_2':
                        self.combo.setCurrentIndex(1)
                elif step.attr['Maxim_ID'] == 'MAXIM_3':
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
            if self.combo.currentIndex() == 0:
                        self.step.attr['Maxim_ID'] = 'MAXIM_1'
            elif self.combo.currentIndex() == 1:
                        self.step.attr['Maxim_ID'] = 'MAXIM_2'
            elif self.combo.currentIndex() == 2:
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
             'Seren 2' : ['None','Cathode 1','Cathode 2','Cathode 3','Cathode 4'],
             'Maxim 1' : ['None','Cathode 1','Cathode 2','Cathode 3','Cathode 4'],
             'Maxim 2' : ['None','Cathode 5','Cathode 6','Cathode 7','Cathode 8'],
             'Maxim 3' : ['None','Cathode 5','Cathode 6','Cathode 7','Cathode 8']         
            }
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.switcherCombo = QComboBox()
                self.switcherCombo.addItems(PowerSwitcher.switcher_supply.keys())
                
                if step.attr['PowerSwitcher_ID'] == 'SWITCHER_1':
                        self.switcherCombo.setCurrentIndex(0)
                elif step.attr['PowerSwitcher_ID'] == 'SWITCHER_2':
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
            if index == 0:
                self.supplyCombo.addItems(self.switcher_supply['Power switcher 1'])
            elif index == 1:
                self.supplyCombo.addItems(self.switcher_supply['Power switcher 2'])
            
            if self.step.attr['PowerSwitcher_InputID'] == 'IN_1':
                self.supplyCombo.setCurrentIndex(0)
            elif self.step.attr['PowerSwitcher_InputID'] == 'IN_2':
                self.supplyCombo.setCurrentIndex(1)

            self.supplyCombo.currentIndexChanged.connect(self.redrawCathodesLayout)
            

        @pyqtSlot(int)
        def redrawCathodesLayout(self,index):
            self.cathodesCombo.clear()
            if self.supplyCombo.itemText(index) == 'Seren 2':
                self.cathodesCombo.addItems(self.supply_cathodes['Seren 2'])
                model = self.cathodesCombo.model()
                item = model.item( 1, 0 )
                item.setEnabled( False) 
            elif self.supplyCombo.itemText(index) == 'Maxim 1':
                self.cathodesCombo.addItems(self.supply_cathodes['Maxim 1'])
                model = self.cathodesCombo.model()
                item = model.item( 2, 0 )
                item.setEnabled( False) 
            elif self.supplyCombo.itemText(index) == 'Maxim 2':
                self.cathodesCombo.addItems(self.supply_cathodes['Maxim 2'])
                model = self.cathodesCombo.model()
                item = model.item( 3, 0 )
                item.setEnabled( False)
            elif self.supplyCombo.itemText(index) == 'Maxim 3':
                self.cathodesCombo.addItems(self.supply_cathodes['Maxim 3'])
                model = self.cathodesCombo.model()
                item = model.item( 2, 0 )
                item.setEnabled( False)

            
            if self.step.attr['PowerSwitcher_OutputID'] == 'NONE':
                        self.cathodesCombo.setCurrentIndex(0)
            elif self.step.attr['PowerSwitcher_OutputID'] == 'OUT_1':
                        self.cathodesCombo.setCurrentIndex(1)
            elif self.step.attr['PowerSwitcher_OutputID'] == 'OUT_2':
                        self.cathodesCombo.setCurrentIndex(2)
            elif self.step.attr['PowerSwitcher_OutputID'] == 'OUT_3':
                        self.cathodesCombo.setCurrentIndex(3)
            elif self.step.attr['PowerSwitcher_OutputID'] == 'OUT_4':
                        self.cathodesCombo.setCurrentIndex(4)
            
        def close(self):
            if self.switcherCombo.currentIndex() == 0 and self.supplyCombo.currentIndex() == 0:
                #Switcher 1 and 1st ouput (SEREN 2) is selected
                self.step.attr["Command_VariableID"] = 'MW_SW1_RF_COMMAND' 
                self.step.attr["State_VariableID"] = 'MW_SW1_RF_STATE'
                self.step.attr["PowerSwitcher_ID"] = 'SWITCHER_1'
                self.step.attr["PowerSwitcher_InputID"] = 'IN_1'
            elif self.switcherCombo.currentIndex() == 0 and self.supplyCombo.currentIndex() == 1:
                #Switcher 1 and 2nd ouput (MAXIM 1) is selected
                self.step.attr["Command_VariableID"] = 'MW_SW1_DC_COMMAND' 
                self.step.attr["State_VariableID"] = 'MW_SW1_DC_STATE'
                self.step.attr["PowerSwitcher_ID"] = 'SWITCHER_1'
                self.step.attr["PowerSwitcher_InputID"] = 'IN_2'
            if self.switcherCombo.currentIndex() == 1 and self.supplyCombo.currentIndex() == 0:
                #Switcher 2 and 1st ouput (MAXIM 2) is selected
                self.step.attr["Command_VariableID"] = 'MW_SW2_RF_COMMAND' 
                self.step.attr["State_VariableID"] = 'MW_SW2_RF_STATE'
                self.step.attr["PowerSwitcher_ID"] = 'SWITCHER_2'
                self.step.attr["PowerSwitcher_InputID"] = 'IN_1'
            elif self.switcherCombo.currentIndex() == 1 and self.supplyCombo.currentIndex() == 1:
                #Switcher 2 and 2nd ouput (MAXIM 3) is selected
                self.step.attr["Command_VariableID"] = 'MW_SW2_DC_COMMAND' 
                self.step.attr["State_VariableID"] = 'MW_SW2_DC_STATE'
                self.step.attr["PowerSwitcher_ID"] = 'SWITCHER_2'
                self.step.attr["PowerSwitcher_InputID"] = 'IN_2'

            if self.cathodesCombo.currentIndex() == 0:
                    #None
                    self.step.attr["PowerSwitcher_OutputID"] = 'NONE'
            elif self.cathodesCombo.currentIndex() == 1:
                    #OUT_1
                    self.step.attr["PowerSwitcher_OutputID"] = 'OUT_1'
            elif self.cathodesCombo.currentIndex() == 2:
                    #OUT_2
                    self.step.attr["PowerSwitcher_OutputID"] = 'OUT_2'
            elif self.cathodesCombo.currentIndex() == 3:
                    #OUT_3
                    self.step.attr["PowerSwitcher_OutputID"] = 'OUT_3'
            elif self.cathodesCombo.currentIndex() == 4:
                    #OUT_4
                    self.step.attr["PowerSwitcher_OutputID"] = 'OUT_4'
            super().close()

class ShutterOpenClose(BaseStepEditor):
        def __init__(self,step,parent=None):
                super().__init__(step,parent)
                self.combo = QComboBox()
                self.combo.addItems(["Cathode {}".format(i) for i in range(1,9)])

                if step.attr['Command_VariableID'] == 'MX_DC_Shutter1_COMMAND':
                        self.combo.setCurrentIndex(0)
                elif step.attr['Command_VariableID'] == 'MX_DC_Shutter2_COMMAND':
                        self.combo.setCurrentIndex(1)
                elif step.attr['Command_VariableID'] == 'MX_DC_Shutter3_COMMAND':
                        self.combo.setCurrentIndex(2)
                elif step.attr['Command_VariableID'] == 'MX_DC_Shutter4_COMMAND':
                        self.combo.setCurrentIndex(3)
                elif step.attr['Command_VariableID'] == 'MX_DC_Shutter5_COMMAND':
                        self.combo.setCurrentIndex(4)
                elif step.attr['Command_VariableID'] == 'MX_DC_Shutter6_COMMAND':
                        self.combo.setCurrentIndex(5)
                elif step.attr['Command_VariableID'] == 'MX_DC_Shutter7_COMMAND':
                        self.combo.setCurrentIndex(6)
                elif step.attr['Command_VariableID'] == 'MX_DC_Shutter8_COMMAND':
                        self.combo.setCurrentIndex(7)

                self.formLayout.addWidget(QLabel("Shutter name"),0,0)
                self.formLayout.addWidget(self.combo,0,1)

                self.buttonGroup = QButtonGroup()
                self.offRadio = QRadioButton('Closed')
                self.onRadio = QRadioButton('Open')
                self.buttonGroup.addButton(self.onRadio)
                self.buttonGroup.addButton(self.offRadio)
                if self.step.attr['OpenState'] == 'true':
                        self.onRadio.setChecked(True)
                elif self.step.attr['OpenState'] == 'false':
                        self.offRadio.setChecked(True)
                self.formLayout.addWidget(QLabel("State"),1,0)
                self.formLayout.addWidget(self.onRadio,1,1)
                self.formLayout.addWidget(self.offRadio,1,2)

        def close(self):
            if self.combo.currentIndex() == 0:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter1_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter1_STATE'
            elif self.combo.currentIndex() == 1:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter2_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter2_STATE'
            elif self.combo.currentIndex() == 2:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter3_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter3_STATE'
            elif self.combo.currentIndex() == 3:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter4_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter4_STATE'
            elif self.combo.currentIndex() == 4:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter5_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter5_STATE'
            elif self.combo.currentIndex() == 5:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter6_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter6_STATE'
            elif self.combo.currentIndex() == 6:
                        self.step.attr['Command_VariableID'] = 'MX_DC_Shutter7_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_Shutter7_STATE'
            elif self.combo.currentIndex() == 7:
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

                if step.attr['Command_VariableID'] == 'MX_DC_BackingValve_COMMAND':
                        self.combo.setCurrentIndex(0)
                elif step.attr['Command_VariableID'] == 'MX_DC_GasInjectionValve_COMMAND':
                        self.combo.setCurrentIndex(1)
                elif step.attr['Command_VariableID'] == 'MX_DC_RoughingValve_COMMAND':
                        self.combo.setCurrentIndex(2)
                elif step.attr['Command_VariableID'] == 'MX_DC_VentingValve_COMMAND':
                        self.combo.setCurrentIndex(3)
                elif step.attr['Command_VariableID'] == 'MX_LL_BackingValve_COMMAND':
                        self.combo.setCurrentIndex(4)
                elif step.attr['Command_VariableID'] == 'MX_LL_VentingValve_COMMAND':
                        self.combo.setCurrentIndex(5)
                elif step.attr['Command_VariableID'] == 'MX_DC_MF1_GasInjectionValve_COMMAND':
                        self.combo.setCurrentIndex(6)
                elif step.attr['Command_VariableID'] == 'MX_DC_MF2_GasInjectionValve_COMMAND':
                        self.combo.setCurrentIndex(7)
                elif step.attr['Command_VariableID'] == 'MX_DC_MF3_GasInjectionValve_COMMAND':
                        self.combo.setCurrentIndex(8)

                self.formLayout.addWidget(QLabel("Valve name"),0,0)
                self.formLayout.addWidget(self.combo,0,1)

                self.buttonGroup = QButtonGroup()
                self.offRadio = QRadioButton('Closed')
                self.onRadio = QRadioButton('Open')
                self.buttonGroup.addButton(self.onRadio)
                self.buttonGroup.addButton(self.offRadio)
                if self.step.attr['OpenState'] == 'true':
                        self.onRadio.setChecked(True)
                if self.step.attr['OpenState'] == 'false':
                        self.offRadio.setChecked(True)
                self.formLayout.addWidget(QLabel("State"),1,0)
                self.formLayout.addWidget(self.onRadio,1,1)
                self.formLayout.addWidget(self.offRadio,1,2)

        def close(self):
            if self.combo.currentIndex() == 0:
                        self.step.attr['Command_VariableID'] = 'MX_DC_BackingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_BackingValve_STATE'
            if self.combo.currentIndex() == 1:
                        self.step.attr['Command_VariableID'] = 'MX_DC_GasInjectionValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_GasInjectionValve_STATE'
            if self.combo.currentIndex() == 2:
                        self.step.attr['Command_VariableID'] = 'MX_DC_RoughingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_RoughingValve_STATE'
            if self.combo.currentIndex() == 3:
                        self.step.attr['Command_VariableID'] = 'MX_DC_VentingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_VentingValve_STATE'
            if self.combo.currentIndex() == 4:
                        self.step.attr['Command_VariableID'] = 'MX_LL_BackingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_LL_BackingValve_STATE'
            if self.combo.currentIndex() == 5:
                        self.step.attr['Command_VariableID'] = 'MX_LL_VentingValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_LL_VentingValve_STATE'
            if self.combo.currentIndex() == 6:
                        self.step.attr['Command_VariableID'] = 'MX_DC_MF1_GasInjectionValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_MF1_GasInjectionValve_STATE'
            if self.combo.currentIndex() == 7:
                        self.step.attr['Command_VariableID'] = 'MX_DC_MF2_GasInjectionValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_MF2_GasInjectionValve_STATE'
            if self.combo.currentIndex() == 8:
                        self.step.attr['Command_VariableID'] = 'MX_DC_MF3_GasInjectionValve_COMMAND'
                        self.step.attr['State_VariableID'] = 'MX_DC_MF3_GasInjectionValve_STATE'
            if self.onRadio.isChecked() : self.step.attr['OpenState'] = 'true' 
            else: self.step.attr['OpenState'] = 'false'
            super().close()