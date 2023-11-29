
from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel,QStyledItemDelegate,QStyleOptionViewItem
from PyQt5.QtCore import pyqtSlot,QObject,QSize,Qt,QAbstractListModel,QModelIndex
from PyQt5.QtGui import QKeySequence,QPainter

#Model
class StepItemModel(QAbstractListModel):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.list=[]
    
    def rowCount(self,parent=QModelIndex()):
        return len(self.list)
    
    def data(self,index,role=Qt.ItemDataRole.DisplayRole):

        return self.list[index.row()]

    def insertRows(self,row,count,parent=QModelIndex()):
        self.beginInsertRows(parent,row,row+count)
        end = self.list.copy()[row:]
        beginning = self.list.copy()[:row]
        self.list = beginning+[None]*count+end
        self.endInsertRows()

    def insertItems(self,row,items):
        self.insertRows(row,len(items))
        for index,item in enumerate(items):
            self.list[row+index] = item

#ItemDelegate
class StepItemDelegate(QStyledItemDelegate):
    def __init__(self,parent = None):
        super().__init__(parent)
    
    def paint(self,painter : QPainter,option:QStyleOptionViewItem,index:QModelIndex):
        super(StyledItemDelegate, self).paint(painter,option,index)
    def sizeHint(self,option:QStyleOptionViewItem,index:QModelIndex):
        return super().sizeHint(option,index)