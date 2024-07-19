import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    try:
        import pyi_splash
        pyi_splash.close()
    except:
        pass
    sys.exit(app.exec())