from PyQt5.QtWidgets import QWidget,QListWidget,QVBoxLayout,QListView,QAbstractItemView


class LibraryWidget(QWidget):
    def __init__(self, parent= None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout()
        self.listWidget= QListWidget()
        #self.listWidget.setSortingEnabled(True)
        self.listWidget.setMovement(QListView.Free)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.debugPopulateList()
        self.layout.addWidget(self.listWidget)

        self.setLayout(self.layout)

    def debugPopulateList(self):
        for i in range(50):
            self.listWidget.addItem("Item {}".format(i))
