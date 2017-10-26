from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtCore import QSize
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT

class ToolWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.__setup_ui()
        self.__connect_slot()


    def __setup_ui(self):
        h_layout = QHBoxLayout()
        #h_layout.setDirection(QBoxLayout.RightToLeft)

        self.__refresh_btn = QPushButton()
        self.__refresh_btn.setIcon(QIcon('./icon/refresh.png'))
        self.__refresh_btn.setIconSize(QSize(20,20))
        self.__refresh_btn.setMaximumSize(30,30)
        self.__refresh_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.__refresh_btn.setFlat(True)


        h_layout.addWidget(self.__refresh_btn,0)
        h_layout.addStretch(1)
        h_layout.setContentsMargins(0,0,0,0)

        self.setLayout(h_layout)

    def __connect_slot(self):
        self.connect(self.__refresh_btn,SIGNAL('clicked()'),self,SLOT('__on_refresh_btn()'))

    @pyqtSlot()
    def __on_refresh_btn(self):
        self.emit(SIGNAL('refresh_btn_clicked()'))