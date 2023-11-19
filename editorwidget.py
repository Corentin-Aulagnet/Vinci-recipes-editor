from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt,QAbstractListModel,QModelIndex
from PyQt5.QtGui import QKeySequence

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
        #self.listView = QListView()
        self.listWidget= QListWidget()
        #self.model = StepItemModel(self.listView)

        #self.listView.setModel(self.model)
        self.listWidget.setMovement(QListView.Free)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)

        self.layout.addWidget(self.listWidget)
        self.setLayout(self.layout)
        self.copyShortcut = QShortcut(QKeySequence("Ctrl+C"),self,self.CopySelected)
        self.copyShortcut = QShortcut(QKeySequence("Ctrl+V"),self,self.PasteSelected)

    def CopySelected(self):
        self.pasteBin = self.listWidget.selectedItems()
    def PasteSelected(self):
        items = []
        for it in self.pasteBin:
            item = QListWidgetItem()
            item.setText(it.text())
            item.setData(Qt.UserRole,it.data(Qt.UserRole))
            items.append(item)
        for index,item in enumerate(items):
            self.listWidget.insertItem(self.listWidget.currentRow()+index,item)
    
    def PopulateList(self,steps):
        self.listWidget.clear()
        for step in steps:
            item = QListWidgetItem()
            item.setText(step['{}type'.format(RecipeEditorWidget.xsi)])
            item.setData(Qt.UserRole,step)
            self.listWidget.addItem(item)

    def GetListItemData(self):
        res = []
        count = self.listWidget.count()
        for i in range(count):
            res.append(self.listWidget.item(i).data(Qt.UserRole))
        return res