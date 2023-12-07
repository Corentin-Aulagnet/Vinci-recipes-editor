from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt,QAbstractListModel,QModelIndex
from PyQt5.QtGui import QKeySequence,QDropEvent,QStandardItemModel,QIcon
from QExpandableItem import QListWidgetView,QExpandableWidget,STRETCHING
from customList import MyListView,MyItem,MyStyledDelegate
from stepeditorwidgets import MassflowSetpoint,VATValve,MaximPowerOff,MaximSetpoints,Sleep,SubstrateHeating,PowerSwitcher,ShutterOpenClose
class RecipeEditorWidget(QWidget):
    xsi='{http://www.w3.org/2001/XMLSchema-instance}'
    def __init__(self,parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.listView = MyListView(self)
        self.model = QStandardItemModel(self.listView)

        self.listView.setModel(self.model)
        self.listView.setDragEnabled(True)
        self.listView.viewport().setAcceptDrops(True)
        self.listView.setDefaultDropAction(Qt.MoveAction)
        self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listView.doubleClicked.connect(self.openStepEditor)
        self.listView.setItemDelegate(MyStyledDelegate(self))
        #self.listView.setMovement(QListView.Free)
        #self.listView.setDragDropMode(QAbstractItemView.DragDrop)
        #self.listWidget.setItemDelegate(StepItemDelegate())

        self.layout.addWidget(self.listView)
        self.setLayout(self.layout)
        self.copyShortcut = QShortcut(QKeySequence("Ctrl+C"),self,self.CopySelected)
        self.copyShortcut = QShortcut(QKeySequence("Ctrl+V"),self,self.PasteSelected)
        self.popup = None

    def ChangeTitle(self,name):
        self.parent().setWindowTitle('Editor - '+name)
    def clear(self):
        self.model.clear()

    def CopySelected(self):
        self.pasteBin = self.listView.selectedIndexes()

    def PasteSelected(self):
        items = []
        for it in self.pasteBin:
            step = it.data(Qt.UserRole)
            item = self.CreateItem(step)
            items.append(item)
        for index,item in enumerate(items):
            self.model.insertRow(self.listView.current.row()+index,item)
    
    def PopulateList(self,steps):
        #self.listWidget.clear()
        self.model.clear()
        for step in steps:
            item = self.CreateItem(step)
            self.model.appendRow(item)
        
    def CreateItem(self,step):
        item = MyItem()
        item.setText(step.type)
        item.setData(step,Qt.UserRole)
        icon = QIcon('res/step_512.png')
        item.setIcon(icon)
        return item
    
    def GetListItemData(self):
        res = []
        count = self.model.rowCount()
        for i in range(count):
            res.append(self.model.item(i).data(Qt.UserRole))
        return res
    @pyqtSlot(QModelIndex)
    def openStepEditor(self,index:QModelIndex):
        step = index.data(Qt.UserRole)
        match step.type:
            case "CParamScript_MassflowSetpoint":
                self.popup = MassflowSetpoint(step,self)
                self.popup.exec()
            case "CParamScript_VatValve":
                self.popup = VATValve(step,self)
                self.popup.exec()
            case "CParamScript_Maxim_PowerOff":
                self.popup = MaximPowerOff(step,self)
                self.popup.exec()
            case "CParamScript_Maxim_Setpoints":
                self.popup = MaximSetpoints(step,self)
                self.popup.exec()
            case "CParamScript_PowerSwitcher":
                self.popup = PowerSwitcher(step,self)
                self.popup.exec()
            case "CParamScript_Sleep":
                self.popup = Sleep(step,self)
                self.popup.exec()
            case "CParamScript_Substrate_HeatingSetpoint":
                self.popup = SubstrateHeating(step,self)
                self.popup.exec()
            case "CParamScript_Shutter_OpenClose":
                self.popup = ShutterOpenClose(step,self)
                self.popup.exec()
                
                
        
        