import sys
import os
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import Qt

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '.'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ui.yt_mainwindow import YtMainWindow


def main():
    app = QApplication(sys.argv)

    #file = open(PROJECT_ROOT + "/styleSheet/styleSheet.qss");
    file = open(os.path.join(os.path.dirname(__file__),'styleSheet/styleSheet.qss'))

    try:
        app.setStyleSheet(file.read());
    finally:
        file.close()

    main_windows = YtMainWindow()
    main_windows.setWindowState(main_windows.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    # main_windows.setWindowState(Qt.WindowMaximized | Qt.WindowActive)
    main_windows.raise_()
    main_windows.show()
    main_windows.activateWindow()

    app.exec_()

if __name__== '__main__':

    sys.exit(main())