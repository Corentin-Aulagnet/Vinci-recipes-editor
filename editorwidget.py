from PyQt5.QtWidgets import QTableView,QWidget,QTabWidget,QVBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QShortcut,QListWidgetItem,QLabel
from PyQt5.QtCore import pyqtSlot,pyqtSignal,QObject,QSize,Qt,QAbstractListModel,QModelIndex
from PyQt5.QtGui import QKeySequence,QDropEvent,QStandardItemModel,QIcon
from QExpandableItem import QListWidgetView,QExpandableWidget,STRETCHING
from customList import CustomView,MyStyledDelegate,CustomModel
from editor import MyTableView
from stepeditorwidgets import StepEditorPopUp,StepAddPopUp
from vincirecipereader import Step,Recipe
from mainwidget import MainWidget

class PasteBinManager():
    copiedItems=[]
            
class RecipeEditorWidget(MainWidget,QWidget):
    xsi='{http://www.w3.org/2001/XMLSchema-instance}'
    def __init__(self,parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.view:MyTableView = MyTableView(self)
        self.view.doubleClicked.connect(self.openStepEditor)


        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        self.copyShortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_C),self,self.CopySelected)
        self.copyShortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_V),self,self.PasteSelected)
        self.tmpStep = Step.dummy()
        self.copyShortcut = QShortcut(QKeySequence(Qt.Key_Return),self,self.AddStep)
        self.copyShortcut = QShortcut(QKeySequence(Qt.Key_Delete),self,self.RemoveStep)
        self.popup = None

    

    def ChangeTitle(self,name):
        self.parent().setWindowTitle('Editor - '+name)
    def clear(self):
        self.model.clear()

    def CopySelected(self):
        pasteBin = [self.view.selectedIndexes()[i] for i in range(1,len(self.view.selectedIndexes()),2)]
        PasteBinManager.copiedItems = []
        for it in pasteBin:
            _step = it.data(Qt.UserRole)
            step = None
            if type(_step) == Step:
                step = Step.from_foo(_step)
            elif type(step) == Recipe:
                step = Recipe.from_foo(_step)
            
            PasteBinManager.copiedItems.append(step)

    def PasteSelected(self):
        for index,step in enumerate(PasteBinManager.copiedItems):
            if(len(self.view.selectedIndexes())> 0): self.view.insertRow(self.view.selectedIndexes()[-1].row()+index+1,step)
            else:self.view.insertRow(index,step)

    def RemoveStep(self):
        indexes = self.view.selectedIndexes()
        if len(indexes)> 0:self.view.removeRows(min([indexes[i].row() for i in range(len(indexes))]),len(indexes)//2)

    def AddStep(self):
        popup = StepAddPopUp(self.tmpStep,self)
        popup.exec()
        if(len(self.view.selectedIndexes()) >=1):
            row = self.view.selectedIndexes()[-1].row()+1
        else: row = 0
        self.view.insertRow(row,Step.from_foo(self.tmpStep))
        
        
    
    def PopulateList(self,steps):
        self.view.model.clear()
        for i,step in enumerate(steps):
            self.view.addRow(step)
            
        
    def CreateItem(self,step,index:QModelIndex):
        item = index
        if(type(step) == Step):
            self.model.setData(item,step.type,Qt.DisplayRole)
            self.model.setData(item,step,Qt.UserRole)
            icon = QIcon('res/step_512.png')
            self.model.setData(item,icon,Qt.DecorationRole)
        elif(type(step) == Recipe):
            item.setText(step.name)
            item.setData(step,Qt.UserRole)
            icon = QIcon('res/ass_512.png')
            item.setIcon(icon)
        return item
    
    def GetListItemData(self):
        res = []
        count = self.view.model.rowCount()
        for i in range(count):
            res.append(self.view.model.item(i,1).data(Qt.UserRole))
        return res
    
    @pyqtSlot(QModelIndex)
    def openStepEditor(self,index:QModelIndex):
        changedRow = index.row()
        firstIndex = self.view.model.index(changedRow,0)
        lastIndex = self.view.model.index(changedRow,1)

        step = lastIndex.data(Qt.UserRole)
        self.popup = StepEditorPopUp(step,self)
        if self.popup.isValid :
            self.popup.exec()
            self.view.updateRow(changedRow,step)
            self.view.model.dataChanged.emit(firstIndex,lastIndex)


class EditorWidget(QTabWidget,MainWidget):
    #currentWidget = None


    def __init__(self,parent=None):
        super().__init__(parent)
        super(MainWidget,self).__init__()
        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideRight)
        self.tabs = []
        self.tabCloseRequested.connect(self.closeTab)

    def addTab(self):
        #EditorWidget.currentWidget = RecipeEditorWidget()
        super().addTab(RecipeEditorWidget(),'New Recipe*')
        self.setCurrentIndex(self.count()-1)
        self.setTabToolTip (self.currentIndex(), 'New Recipe*')
        #self.setIconSize(QSize(50,50))

    def changeCurrentTab(self,steps,title,type):
        if(self.count()==0 or self.tabText(self.currentIndex())!='New Recipe*' ):
            self.addTab()
        self.widget(self.currentIndex()).PopulateList(steps)
        if type == Step:
            self.setTabIcon(self.currentIndex(),QIcon('res/step_512.png'))
        elif type == Recipe:
            self.setTabIcon(self.currentIndex(),QIcon('res/ass_512.png'))
        
        self.ChangeTitleofTab(title)
    def isAlreadyOpen(self,title):
        for i in range(self.count()):
            if(self.tabText(i) == title):
                return True
        return False
    def setCurrentIndex(self,index:int):
        #EditorWidget.currentWidget = self.currentWidget
        super().setCurrentIndex(index)
    def switchTo(self,title):
        for i in range(self.count()):
            if(self.tabText(i) == title):
                self.setCurrentIndex(i)
    
    @pyqtSlot(int)
    def closeTab (self, currentIndex):
        currentQWidget = self.widget(currentIndex)
        currentQWidget.deleteLater()
        self.removeTab(currentIndex)
    
    def ChangeTitleofTab(self,title):
        self.setTabText(self.currentIndex(), title)
        self.setTabToolTip (self.currentIndex(), title)
    
    def GetCurrentList(self):
        #EditorWidget.currentQWidget = self.widget(self.currentIndex())
        return self.currentWidget().GetListItemData()


        
                
                
        
        