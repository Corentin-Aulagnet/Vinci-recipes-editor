from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt,QAbstractListModel,QModelIndex
from PyQt5.QtGui import QKeySequence
from QExpandableItem import QListWidgetView,QExpandableWidget,STRETCHING
class StepItemModel(QAbstractListModel):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.list=[]
    
    def rowCount(self,parent=QModelIndex()):
        return len(self.list)
    
    def data(index,role=Qt.ItemDataRole.DisplayRole):
        return self.list[index]

    def insertItems(row,count,parent=QModelIndex()):
        self.beginInsertRows()
        temp = self.list.copy()[row:]
        self.list = self.list[:row]+parent+temp
            
        self.endInsertRows()
class RecipeEditorWidget(QWidget):
    xsi='{http://www.w3.org/2001/XMLSchema-instance}'
    def __init__(self,parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.listView = QListWidgetView(self)
        #self.listWidget= QListWidget()
        #self.model = StepItemModel(self.listView)

        #self.listView.setModel(self.model)
        self.listView.setMovement(QListWidget.Free)
        self.listView.setDragDropMode(QAbstractItemView.InternalMove)

        self.layout.addWidget(self.listView)
        self.setLayout(self.layout)
        self.copyShortcut = QShortcut(QKeySequence("Ctrl+C"),self,self.CopySelected)
        self.copyShortcut = QShortcut(QKeySequence("Ctrl+V"),self,self.PasteSelected)

    def CopySelected(self):
        self.pasteBin = self.listView.selectedItems()
    def PasteSelected(self):
        items = []
        for it in self.pasteBin:
            item = QExpandableWidget(it.title)
            #item.setText(it.text())
            item.setData(it.getData())
            items.append(item)
        for index,item in enumerate(items):
            self.listView.insertItem(self.listView.currentRow()+index,item)
    
    def PopulateList(self,steps):
        self.listView.clear()
        for step in steps:
            
            item = QExpandableWidget(step.type,animated=False)
            
            b=QLabel()
            b.setText("test")
            item.setContents(b)
            self.listView.addWidget(item)

    def GetListItemData(self):
        res = []
        count = self.listView.count()
        for i in range(count):
            res.append(self.listView.item(i).widget.getData())
        return res