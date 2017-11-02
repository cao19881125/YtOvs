from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import pyqtSlot

class DbTreeHeaderWidget(QWidget):
    def __init__(self, header_label,item,con_key):
        QWidget.__init__(self)
        self.__item = item
        self.__con_key = con_key
        self.__setup_ui(header_label)
        self.__connect_slot()

    def __setup_ui(self,header_label):
        la = QHBoxLayout()
        self.__close_btn = QPushButton()
        self.__close_btn.setIcon(QIcon('./icon/close.png'))
        self.__close_btn.setIconSize(QSize(15, 15))
        self.__close_btn.setMaximumSize(20, 20)
        self.__close_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.__close_btn.setFlat(True)
        la.addWidget(QLabel(header_label), 1)
        la.addWidget(self.__close_btn, 0)
        la.setContentsMargins(0, 0, 0, 0)
        self.setLayout(la)

    def __connect_slot(self):
        self.connect(self.__close_btn,SIGNAL('clicked()'),self,SLOT('__on_close_btn()'))

    @pyqtSlot()
    def __on_close_btn(self):
        self.emit(SIGNAL('close_btn_clickd(PyQt_PyObject,PyQt_PyObject)'),self.__item,self.__con_key)