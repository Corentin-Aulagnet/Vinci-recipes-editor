from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItem,QDragEnterEvent,QDragMoveEvent,QDropEvent,QMouseEvent,QDrag
from PyQt5.QtCore import Qt,QModelIndex
class MyListView(QListView):


    def __init__(self,parent=None):
        super().__init__(parent)
        self.current = None

    def currentChanged(self,current,previous):
        self.current = current
    def dropEvent(self,event:QDropEvent):
        if event.keyboardModifiers() == Qt.ControlModifier:
            event.setDropAction(Qt.CopyAction)
        if event.source() == self and (Qt.MoveAction and event.possibleActions()):
            #Drag and Drop within widget
            if(event.proposedAction() == Qt.MoveAction):
                print("MoveAction")
                event.acceptProposedAction()
                insertPos   = event.pos()
                fromList    = event.source()
                #insertRow   = fromList.model().itemFromIndex(fromList.indexAt( insertPos ))
                insertRow   = self.indexAt( insertPos ).row()
                mimeData = event.mimeData()
                self.model().dropMimeData(event.mimeData(),Qt.MoveAction,insertRow+1,0,QModelIndex())
            elif event.proposedAction() == Qt.CopyAction:
                print("CopyAction")
                event.acceptProposedAction()
                insertPos   = event.pos()
                fromList    = event.source()
                #insertRow   = fromList.model().itemFromIndex(fromList.indexAt( insertPos ))
                insertRow   = self.indexAt( insertPos ).row()
                mimeData = event.mimeData()
                self.model().dropMimeData(event.mimeData(),Qt.MoveAction,insertRow+1,0,QModelIndex())
            else:
                return

class MyItem(QStandardItem):
    def __init__(self,parent=None):
        super().__init__(parent)
