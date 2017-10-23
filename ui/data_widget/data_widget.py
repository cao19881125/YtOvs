from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from data_item_widget import DataItemWidget

class DataWidget(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        self.__setup_ui()
        self.__connect_slot()

    def __setup_ui(self):
        self.setTabsClosable(True)


    def add_tab(self, con_key, table_name):
        widget = DataItemWidget(con_key, table_name)
        self.addTab(widget, table_name)
        self.setCurrentWidget(widget)

    def __connect_slot(self):
        self.connect(self,SIGNAL('tabCloseRequested (int)'), self, SLOT('__on_tab_close(int)'))

    @pyqtSlot('int')
    def __on_tab_close(self,index):
        self.removeTab(index)