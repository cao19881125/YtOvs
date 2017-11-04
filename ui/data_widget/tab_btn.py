from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QSize

class TabBtn(QPushButton):
    def __init__(self, icon_path):
        QPushButton.__init__(self)
        self.__icon_path = icon_path
        self.__setup_ui()

    def __setup_ui(self):
        self.setMaximumSize(20,20)
        self.setIcon(QIcon(self.__icon_path))
        self.setIconSize(QSize(15,15))
        self.setFlat(True)




