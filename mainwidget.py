from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
class MainWidget(QWidget):
    messageChanged = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)