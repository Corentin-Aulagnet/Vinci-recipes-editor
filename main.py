import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from mainwindow import MainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())