from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt,QAbstractListModel,QModelIndex
from PyQt5.QtGui import QKeySequence
from QExpandableItem import QListWidgetView,QExpandableWidget,STRETCHING
from customList import StepItemModel,StepItemDelegate
class RecipeEditorWidget(QWidget):
    xsi='{http://www.w3.org/2001/XMLSchema-instance}'
    def __init__(self,parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        #self.listView = QListView(self)
        self.listWidget= QListWidget()
        #self.model = StepItemModel(self.listView)

        #self.listView.setModel(self.model)
        self.listWidget.setMovement(QListWidget.Free)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        #self.listWidget.setItemDelegate(StepItemDelegate())

        self.layout.addWidget(self.listWidget)
        self.setLayout(self.layout)
        self.copyShortcut = QShortcut(QKeySequence("Ctrl+C"),self,self.CopySelected)
        self.copyShortcut = QShortcut(QKeySequence("Ctrl+V"),self,self.PasteSelected)

    def CopySelected(self):
        self.pasteBin = self.listWidget.selectedItems()
    def PasteSelected(self):
        items = []
        for it in self.pasteBin:
            item = QExpandableWidget(it.title)
            #item.setText(it.text())
            item.setData(it.getData())
            items.append(item)
        for index,item in enumerate(items):
            self.listWidget.insertItem(self.listWidget.currentRow()+index,item)
    
    def PopulateList(self,steps):
        self.listWidget.clear()
        for step in steps:
            item = QListWidgetItem()
            item.setText(step.type)
            print(step.type)
            item.setData(Qt.UserRole,step)
            self.listWidget.addItem(item)
            
            '''
            item = QExpandableWidget(step.type,animated=False)
            
            b=QLabel()
            b.setText("test")
            item.setContents(b)
            '''
            #self.listView.addWidget(item)
        

    def GetListItemData(self):
        res = []
        count = self.listView.count()
        print('re')
        for i in range(count):
            res.append(self.listView.item(i).data(Qt.UserRole))
        return res