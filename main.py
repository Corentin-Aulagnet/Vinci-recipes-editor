import sys
from PyQt5.QtWidgets import QApplication
from mainwidget import MainWidget
from mainwindow import MainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    try:
        import pyi_splash
        pyi_splash.close()
    except:
        pass
    app.lastWindowClosed.connect(MainWidget.savePrefs)
    sys.exit(app.exec())