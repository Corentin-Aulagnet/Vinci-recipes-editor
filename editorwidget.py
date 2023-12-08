from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt,QAbstractListModel,QModelIndex
from PyQt5.QtGui import QKeySequence,QDropEvent,QStandardItemModel,QIcon
from QExpandableItem import QListWidgetView,QExpandableWidget,STRETCHING
from customList import MyListView,MyItem,MyStyledDelegate
from stepeditorwidgets import StepEditorPopUp,StepAddPopUp
from vincirecipereader import Step,Recipe
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
        self.copyShortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_C),self,self.CopySelected)
        self.copyShortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_V),self,self.PasteSelected)
        self.tmpStep = Step()
        self.copyShortcut = QShortcut(QKeySequence(Qt.Key_Return),self,self.AddStep)
        self.copyShortcut = QShortcut(QKeySequence(Qt.Key_Delete),self,self.RemoveStep)
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
            if(self.listView.current != None): self.model.insertRow(self.listView.current.row()+index+1,item)

    def RemoveStep(self):
        indexes = self.listView.selectedIndexes()
        if len(indexes)> 0:self.model.removeRows(indexes[0].row(),len(indexes))

    def AddStep(self):
        self.tmpStep = Step()
        popup = StepAddPopUp(self.tmpStep,self)
        popup.exec()
        item = self.CreateItem(self.tmpStep)
        row = -1
        if(self.listView.current != None):
            row = self.listView.current.row()
        if row == -1 : row = 0
        self.model.insertRow(row,item)
    
    def PopulateList(self,steps):
        #self.listWidget.clear()
        self.model.clear()
        for step in steps:
            item = self.CreateItem(step)
            self.model.appendRow(item)
        
    def CreateItem(self,step):
        item = MyItem()
        if(type(step) == Step):
            item.setText(step.type)
            item.setData(step,Qt.UserRole)
            icon = QIcon('res/step_512.png')
            item.setIcon(icon)
        elif(type(step) == Recipe):
            item.setText(step.name)
            item.setData(step,Qt.UserRole)
            icon = QIcon('res/ass_512.png')
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
        self.popup = StepEditorPopUp(step,self)
        self.popup.exec()
        
                
                
        
        