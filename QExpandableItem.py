from PyQt5.QtWidgets import QLabel,QWidget,QListWidget,QVBoxLayout,QHBoxLayout,QListView,QAbstractItemView,QPushButton,QFileDialog,QToolButton,QListWidgetItem
from PyQt5.QtCore import pyqtSlot,pyqtSignal,QObject,QSize,QPropertyAnimation,QTime,Qt,QSize,QCoreApplication,QEventLoop
from enum import Enum
class STRETCHING(Enum):
    NONE = 0
    TO_LEFT = 1 
    TO_CENTER = 2
    TO_RIGHT = 3
class QExpandableWidget(QWidget) :
    heightChanged = pyqtSignal(int)
    def __init__(self,title, parent = None, toggle = None, header = None, body = None, expand_height = 0, animated = False, toggleAnimation = None, duration = 200):
        super().__init__(parent)
        self.toggle = toggle
        
        self. title = title
        
        self.header = header 
        self.body = body
        self.expand_height = expand_height
        self.animated = animated
        self.toggleAnimation = toggleAnimation
        self.duration = duration
        self.init_toggle(title)
    def setTitle(self,title):
        self.toggle.setText(title)
        self.title = title
    def setContents(self,b:QWidget,h:QWidget = None, header_stretching = STRETCHING.TO_LEFT):
        if(self.body != None):
            print("qt_ext::QExpandableWidget::setContent : Already existing content -> nothing to be done")
            #qWarning() << "qt_ext::QExpandableWidget::setContent : Already existing content -> nothing to be done";
        elif(b == None):
            print("qt_ext::QExpandableWidget::setContent : No body given -> nothing to be done")
            #qWarning() << "qt_ext::QExpandableWidget::setContent : No body given -> nothing to be done";
        else:
        
            self.header = h
            self.body = b
            
            outer_layout =  QVBoxLayout()
            inner_layout = QHBoxLayout()

            if(header_stretching == STRETCHING.TO_RIGHT or header_stretching == STRETCHING.TO_CENTER):
                inner_layout.addStretch()

            inner_layout.addWidget(self.toggle)

            if(self.header != None):
                inner_layout.addWidget(self.header)

            if(header_stretching == STRETCHING.TO_LEFT or header_stretching == STRETCHING.TO_CENTER):
                inner_layout.addStretch()

            outer_layout.addLayout(inner_layout)
            outer_layout.addWidget(self.body)
            #outer_layout.addStretch()

            self.expand_height = self.body.sizeHint().height()
            self.body.setMaximumHeight(0); # collapse

            self.setLayout(outer_layout)

            if(self.animated):
                self.init_animation()
        
    
    def clearContents(self):
        if(self.animated):
            self.toggleAnimation = None
        
        self.title = self.toggle.text()

        self.init_toggle(self.title)

        if(self.header != None):
            self.header = None
        if(self.body != None):
            self.body = None

    def isAnimated(self):
        return self.animated
    
    def getDuration(self):

        return self.duration

    def  getHeader(self):
        return self.header

    def getBody(self):
    
        return self.body
    
    def getToggle(self):
    
        return self.toggle
    
    def init_toggle(self,title):
    
        if(self.toggle == None):
        
            self.toggle = QToolButton(self)
            self.toggle.setStyleSheet("QToolButton { border: none; }")
            self.toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.toggle.setArrowType(Qt.ArrowType.RightArrow)
            self.toggle.setText(self.title)
            self.toggle.setCheckable(True)
            self.toggle.setChecked(False)
            self.toggle.toggled.connect(self.expand_collapse)
        
    def init_animation(self):
    
        if(self.toggleAnimation == None):
        
            self.toggleAnimation = QPropertyAnimation(self.body, b"maximumHeight", self)
            self.toggleAnimation.setDuration(int(self.duration))
        
    @pyqtSlot(bool)
    def expand_collapse(self,checked):
        if(self.body != None):
            if(checked):
            
                self.toggle.setArrowType(Qt.ArrowType.DownArrow)
                if(not self.animated):
                    self.body.setMaximumHeight(self.expand_height)
                else:
                
                    self.toggleAnimation.setStartValue(0)
                    self.toggleAnimation.setEndValue(self.expand_height)
                    self.toggleAnimation.start()
                
                self.heightChanged.emit(self.expand_height)
            
            else:
            
                self.toggle.setArrowType(Qt.ArrowType.RightArrow)
                if(not self.animated):
                    self.body.setMaximumHeight(0)
                else:
                
                    self.toggleAnimation.setStartValue(self.expand_height)
                    self.toggleAnimation.setEndValue(0)
                    self.toggleAnimation.start()
                self.heightChanged.emit(-self.expand_height)

        

class QListWidgetView(QListWidget) :
    def __init__ (self,parent):
        super().__init__(parent)
    def addWidget(self,ew:QExpandableWidget):
    
        item = QListWidgetItem(self)
        self.addItem(item)
        item.setSizeHint(ew.sizeHint())
        self.setItemWidget(item, ew)
        
        if(type(ew) == QExpandableWidget): ew.heightChanged.connect(self.itemHeightChanged)
    
    @pyqtSlot(int)
    def itemHeightChanged(self,delta):
        ew = self.sender()
        if(ew != None):
            found = False
            i = 0
            while(not found and  i < self.count()):
            
                if(self.itemWidget(self.item(i)) == ew):
                    found = True
                else:
                    i+=1
            
            if(ew.isAnimated() and (delta < 0)):
            
                dieTime = QTime.currentTime().addMSecs(int(ew.getDuration()))
                while(QTime.currentTime() < dieTime):
                    QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
            
            self.item(i).setSizeHint(QSize(ew.sizeHint().width(), self.item(i).sizeHint().height()+delta))
        