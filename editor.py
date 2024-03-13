from PyQt5.QtGui import QStandardItemModel,QStandardItem,QIcon,QDropEvent
from PyQt5.QtWidgets import QProxyStyle,QStyleOption,QTableView,QHeaderView,QAbstractItemView
from PyQt5.QtCore import Qt,QModelIndex
from vincirecipereader import Step,Recipe
class MyModel(QStandardItemModel):

    def dropMimeData(self, data, action, row, col, parent):
        """
        Always move the entire row, and don't allow column "shifting"
        """
        
        return super().dropMimeData(data, action, row, 0, parent)

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
        self.viewport().setAcceptDrops(True)
        self.setDragDropMode(self.InternalMove)
        self.setDragDropOverwriteMode(False)

        # Set our custom style - this draws the drop indicator across the whole row
        self.setStyle(MyStyle())

        # Set our custom model - this prevents row "shifting"
        self.model = MyModel()
        self.setModel(self.model)
    

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
        super().dropEvent(event)
        #event.accept()
        #mimeData = event.mimeData()
        
        #self.model.dropMimeData(mimeData,Qt.CopyAction,insertRow,0,QModelIndex())

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
        
        item_2 = QStandardItem(str(step.attr))
        item_2.setEditable(False)
        item_2.setDropEnabled(False)
        item_2.setData(step,Qt.UserRole)
        return [item_1, item_2]
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