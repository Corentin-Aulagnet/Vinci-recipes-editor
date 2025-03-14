from PyQt5.QtGui import QStandardItemModel,QStandardItem,QIcon,QDropEvent
from PyQt5.QtWidgets import QProxyStyle,QStyleOption,QTableView,QHeaderView,QAbstractItemView
from PyQt5.QtCore import Qt,QModelIndex,QTextStream,QIODevice,QMimeData
from vincirecipereader import Step,Recipe
from mainwidget import MainWidget
class MyModel(QStandardItemModel):

    def dropMimeData(self, data, action, row, col, parent):
        """
        Always move the entire row, and don't allow column "shifting"
        """
        return super().dropMimeData(data, Qt.CopyAction, row, 0, parent)
    
class MyStyle(QProxyStyle):

    def drawPrimitive(self, element, option, painter, widget=None):
        """
        Draw a line across the entire row rather than just the column
        we're hovering over.  This may not always work depending on global
        style - for instance I think it won't work on OSX.
        """
        if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            option_new = QStyleOption(option)
            option_new.rect.setLeft(0)
            if widget:
                option_new.rect.setRight(widget.width())
            option = option_new
        super().drawPrimitive(element, option, painter, widget)
class MyMimeData(QMimeData):
     def __init__(self,mimeType,data):
        self.mimeType = mimeType
        self.data = data
        super().__init__()    
        
     def hasFormat(self,mimeType:str)->bool:
        return mimeType == 'StepInfo' or mimeType == 'RecipeInfo' or super().hasFormat(mimeType)
     def formats(self):
        return ['StepInfo','RecipeInfo']+super().formats()
     def retrieveData(self,mimeType:str,type):
        if mimeType == 'StepInfo' and type == Step and self.hasFormat(mimeType):
            return self.data
        if mimeType == 'RecipeInfo' and type == Recipe and self.hasFormat(mimeType):
            return self.data
        else:
            return super().retrieveData(mimeType,type)
          
class MyTableView(QTableView):

    def __init__(self, parent):
        super().__init__(parent)
        self.verticalHeader()
        self.horizontalHeader()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.ExtendedSelection)
        self.setShowGrid(False)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(self.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropOverwriteMode(False)
        self.setAcceptDrops(True)

        # Set our custom style - this draws the drop indicator across the whole row
        self.setStyle(MyStyle())

        # Set our custom model - this prevents row "shifting"
        self.model = MyModel()
        self.setModel(self.model)

    def dragEnterEvent(self, event):
        event.accept()
        

    '''def dragMoveEvent(self, event):
        event.accept()'''

    def dragLeaveEvent(self,event):
        super().dragLeaveEvent(event)

    def dropEvent(self,event):
        insertRow   = self.indexAt( event.pos() ).row()
        if self.dropIndicatorPosition() == QAbstractItemView.OnItem:
            #do nothing
            return
        elif self.dropIndicatorPosition() == QAbstractItemView.AboveItem:
                        #Above the item
                        insertRow   = self.indexAt( event.pos() ).row()
        elif self.dropIndicatorPosition() == QAbstractItemView.BelowItem:
                        #Below the item
                        insertRow   = self.indexAt( event.pos() ).row() + 1
        elif self.dropIndicatorPosition() == QAbstractItemView.OnViewport:
                        #At the end
                        insertRow   = self.model.rowCount()
        if event.source() == self:
            if event.keyboardModifiers() == Qt.ControlModifier:
                event.setDropAction(Qt.CopyAction)
            else:
                event.setDropAction(Qt.MoveAction)
            
            data=[]
            for index in [event.source().selectedIndexes()[i] for i in range(1,len(event.source().selectedIndexes()),2)]: 
                if(event.dropAction() == Qt.CopyAction):
                    d = index.data(Qt.UserRole)
                    if type(d) == Step:
                        data.append(Step.from_foo(index.data(Qt.UserRole)))
                    else : 
                        data.append(Recipe.from_foo(index.data(Qt.UserRole)))
                else:
                    data.append(index.data(Qt.UserRole))     
        #super().dropEvent(event)
        else:
            data = event.source().selectedIndexes()[0].data(Qt.UserRole)
        event.accept()
        self.insertRows(insertRow,data)
        #self.model.dropMimeData(event.mimeData(),event.dropAction(),insertRow,0,self.indexAt( event.pos() ))

    def addRow(self,step):
        
        item = self.createItem(step)
        
        self.model.appendRow(item)

    def insertRows(self,start,rows):
        for i,row in enumerate(rows):
            self.insertRow(start+i,row)

    def insertRow(self,start,step):
        item = self.createItem(step)
        self.model.insertRow(start,item)

    def removeRows(self,start,count):
        self.model.removeRows(start,count)
        
    def removeRow(self,row):
        self.removeRows(row,1)
        
    def createStepItem(self,step:Step):
        item_1 = QStandardItem(step.name)
        item_1.setEditable(False)
        item_1.setDropEnabled(False)
        icon = QIcon('res/step_512.png')
        item_1.setData(icon,Qt.DecorationRole)
        
        item_2 = QStandardItem(self.getInfos(step))
        item_2.setEditable(False)
        item_2.setDropEnabled(False)
        item_2.setData(step,Qt.UserRole)
        return [item_1, item_2]
    
    def getInfos(self,step:Step):
        name = step.name
        infos=""
        if(name =="MassflowSetpoint"):
            infos = "{} , Setpoint = {}sccm".format(step.attr["Massflow_ID"],step.attr["SetPoint_sccm"])
        elif name == "VatValve":
            mode = step.attr["Mode"]
            if mode == "PositionControl":
                unit = "%"
            elif mode == "PressureControl":
                unit = "mbar"
            else : unit = ""
            infos = "Mode : {} , Setpoint = {}{}".format(mode,step.attr['Setpoint'],unit)
        elif name == "Maxim_PowerOff":
            state = "OFF"
            if bool(step.attr["IsOn"] == "true"):state = "ON"
            infos = "{} , {}".format(step.attr["Maxim_ID"],state)
        elif name == "Maxim_Setpoints":
            infos = "{} , P={}W, I={}A, Voltage={}V, ramp={}s, arc delay={}us, arc offtime={}us".format(step.attr["Maxim_ID"],step.attr["Power"],step.attr["Current"],step.attr["Voltage"],step.attr["RampTime"],step.attr["ArcDetectDelayTime"],step.attr["ArcOffTime"])
        elif name == "PowerSwitcher":
            swInputId={'SWITCHER_1':{'IN_1':'SEREN 2', 'IN_2':'MAXIM 1'},'SWITCHER_2':{'IN_1':'MAXIM 2','IN_2':'MAXIM 3'}}
            supply_cathodes= {
             'SEREN 2' : {'NONE':'None','OUT_1':'Cathode 1 ({})'.format(MainWidget.target_symbols[0]),'OUT_2':'Cathode 2 ({})'.format(MainWidget.target_symbols[1]),'OUT_3':'Cathode 3 ({})'.format(MainWidget.target_symbols[2]),'OUT_4':'Cathode 4 ({})'.format(MainWidget.target_symbols[3])},
             'MAXIM 1' : {'NONE':'None','OUT_1':'Cathode 1 ({})'.format(MainWidget.target_symbols[0]),'OUT_2':'Cathode 2 ({})'.format(MainWidget.target_symbols[1]),'OUT_3':'Cathode 3 ({})'.format(MainWidget.target_symbols[2]),'OUT_4':'Cathode 4 ({})'.format(MainWidget.target_symbols[3])},
             'MAXIM 2' : {'NONE':'None','OUT_1':'Cathode 5 ({})'.format(MainWidget.target_symbols[4]),'OUT_2':'Cathode 6 ({})'.format(MainWidget.target_symbols[5]),'OUT_3':'Cathode 7 ({})'.format(MainWidget.target_symbols[6]),'OUT_4':'Cathode 8 ({})'.format(MainWidget.target_symbols[7])},
             'MAXIM 3' : {'NONE':'None','OUT_1':'Cathode 5 ({})'.format(MainWidget.target_symbols[4]),'OUT_2':'Cathode 6 ({})'.format(MainWidget.target_symbols[5]),'OUT_3':'Cathode 7 ({})'.format(MainWidget.target_symbols[6]),'OUT_4':'Cathode 8 ({})'.format(MainWidget.target_symbols[7])}         
            }
            supply = (swInputId[step.attr['PowerSwitcher_ID']])[step.attr['PowerSwitcher_InputID']]
            infos = "Switcher: {}, Supplier: {}, Output: {}".format(step.attr['PowerSwitcher_ID'],supply,supply_cathodes[supply][step.attr["PowerSwitcher_OutputID"]])
        elif name == "Sleep":
            infos = "Wait {}s".format(step.attr["WaitTime_Sec"])
        elif name == "Substrate_HeatingOff":
             infos = ""
        elif name == "Substrate_HeatingOn":
             infos = ""
        elif name == "Substrate_RotationOff":
             infos = ""
        elif name == "Substrate_RotationOn":
             infos = ""
        elif name == "Substrate_HeatingSetpoint":
            infos = "Heat setpoint {}°C".format(step.attr["SetPoint_Deg"])
        elif name == "Shutter_OpenClose":
            step2Cathode = {'MX_DC_Shutter{}_COMMAND'.format(i,):'Cathode {} ({})'.format(i,MainWidget.target_symbols[i-1]) for i in range(1,9)}
            state= 'OPEN'
            if step.attr['OpenState'] == 'false':
                state = 'CLOSE'
            
            infos = "{} {}".format(step2Cathode[step.attr['Command_VariableID']],state)
        elif name == "Valve_OpenClose":
            step2Valve={'MX_DC_BackingValve_COMMAND':"Deposit chamber Backing valve",
                                     'MX_DC_GasInjectionValve_COMMAND':"Deposit chamber Gas injection valve",
                                     'MX_DC_RoughingValve_COMMAND':"Deposit chamber Roughing valve",
                                     'MX_DC_VentingValve_COMMAND':"Deposit chamber Venting valve",
                                     'MX_LL_BackingValve_COMMAND':"Loadlock chamber Backing valve",
                                     'MX_LL_VentingValve_COMMAND':"Loadlock chamber Venting valve",
                                     'MX_DC_MF1_GasInjectionValve_COMMAND':"Massflow #1 Gas injection valve",
                                     'MX_DC_MF2_GasInjectionValve_COMMAND':"Massflow #2 Gas injection valve",
                                     'MX_DC_MF3_GasInjectionValve_COMMAND':"Massflow #3 Gas injection valve"}
            state = 'OPEN'
            if step.attr['OpenState'] == 'false':
                state = 'CLOSE'
            infos = "{} {}".format(step2Valve[step.attr['Command_VariableID']],state)
        elif name == "Seren_PowerOff":
            if step.attr["IsOn"]=='true':
                state = "On"
            else: state = "Off"
            infos = "{} : {}".format(step.attr["SerenID"],state)
        #elif name == "Seren_MC2_Setpoints":
        #elif name == "Seren_Rx01_Setpoints":
        return infos
    def createRecipeItem(self,recipe:Recipe):
        item_1 = QStandardItem(recipe.name)
        item_1.setEditable(False)
        item_1.setDropEnabled(False)
        icon = QIcon('res/ass_512.png')
        item_1.setData(icon,Qt.DecorationRole)
        
        item_2 = QStandardItem(recipe.path)
        item_2.setEditable(False)
        item_2.setDropEnabled(False)
        item_2.setData(recipe,Qt.UserRole)
        return [item_1, item_2]
    
    def createItem(self,step):
        if(type(step) == Step):
            return self.createStepItem(step)  
        else: 
            return self.createRecipeItem(step)
        
    def updateRow(self,row,step):
        self.model.removeRow(row)
        self.insertRow(row,step)