from PyQt5.QtWidgets import QTableView,QListView,QStyledItemDelegate,QStyleOptionViewItem,QAbstractItemView
from PyQt5.QtGui import QStandardItem,QDragEnterEvent,QDragMoveEvent,QDropEvent,QMouseEvent,QDrag,QPainter
from PyQt5.QtCore import Qt,QModelIndex,QAbstractTableModel,QVariant
from vincirecipereader import Recipe
class CustomView(QTableView):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.currentRow = None

    def currentChanged(self,current,previous):
        self.currentRow = current
    def dropEvent(self,event:QDropEvent):
        if event.keyboardModifiers() == Qt.ControlModifier:
            event.setDropAction(Qt.CopyAction)
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
                        insertRow   = self.model.rowCount() + 1
        if event.source() == self and (Qt.MoveAction and event.possibleActions()):
            #Drag and Drop within widget
            if(event.proposedAction() == Qt.MoveAction):
                event.acceptProposedAction()
                insertPos   = event.pos()
                fromList    = event.source()
                #insertRow   = fromList.model().itemFromIndex(fromList.indexAt( insertPos ))
                #insertRow   = self.indexAt( insertPos ).row()
                mimeData = event.mimeData()
                self.model().dropMimeData(event.mimeData(),Qt.MoveAction,insertRow,0,QModelIndex())
            elif event.proposedAction() == Qt.CopyAction:
                event.acceptProposedAction()
                insertPos   = event.pos()
                fromList    = event.source()
                #insertRow   = fromList.model().itemFromIndex(fromList.indexAt( insertPos ))
                #insertRow   = self.indexAt( insertPos ).row()
                mimeData = event.mimeData()
                self.model().dropMimeData(event.mimeData(),Qt.MoveAction,insertRow,0,QModelIndex())
            else:
                return
        else:
            insertPos   = event.pos()
            fromList    = event.source()
            insertitem  = fromList.itemFromIndex(fromList.indexAt( insertPos ))
            #insertRow   = self.indexAt( insertPos ).row()
            mimeData = event.mimeData()
            self.model().dropMimeData(mimeData,Qt.MoveAction,insertRow,0,QModelIndex())

class MyStyledDelegate(QStyledItemDelegate):
    def __init__(self,parent= None):
        super().__init__(parent)
    
    def paint(self,painter:QPainter, option:QStyleOptionViewItem, index:QModelIndex):
        super().paint(painter,option,index)


class CustomModel(QAbstractTableModel):
    def __init__(self,parent):
        super().__init__(parent)
        self.datas=[]

    def rowCount(self,parent:QModelIndex=QModelIndex()):
        if(parent.isValid()):
            return 0
        else: 
              return len(self.datas)
    def columnCount(self,parent:QModelIndex=QModelIndex()):
          return 2
    
    def setData(self,index,value,role:Qt.DisplayRole):
        self.dataChanged.emit(index,index,[role])

    def data(self,index:QModelIndex, role:int = Qt.DisplayRole):
          if(index.isValid):
                return "Ok"#index.data(role)
          else:
                return QVariant() #invalid QVariant
    def headerData(self,section:int,orientation,role=Qt.DisplayRole):
          return "header "+str(section)
    def insertRows(self,row:int,count:int,parent:QModelIndex = QModelIndex()):
        try:
            self.beginInsertRows(parent,row,row+count)
            tmp_start = self.datas[:row]
            tmp_end = self.datas[row:]
            tmp_start.append(parent)
            self.datas=tmp_start+tmp_end
            self.endInsertRows()
            return True
        except:
            return False
    def insertRow(self,row:int,parent:QModelIndex = QModelIndex()):
        self.insertRows(row,1,parent)
    def flags(self,index:QModelIndex):
         return Qt.ItemIsSelectable | Qt.ItemIsEnabled
