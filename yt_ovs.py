import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import Qt
from ui.yt_mainwindow import YtMainWindow

if __name__== '__main__':
    app = QApplication(sys.argv)

    file = open("./styleSheet/styleSheet.qss");
    try:
        app.setStyleSheet(file.read());
    finally:
        file.close()

    main_windows = YtMainWindow()
    main_windows.setWindowState(main_windows.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    #main_windows.setWindowState(Qt.WindowMaximized | Qt.WindowActive)
    main_windows.raise_()
    main_windows.show()
    main_windows.activateWindow()



    sys.exit(app.exec_())