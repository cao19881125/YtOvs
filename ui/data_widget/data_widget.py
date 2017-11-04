from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTabBar
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from data_item_widget import DataItemWidget
from tab_btn import TabBtn
from ui.yt_icon.icon_manager import IconManager

class DataWidget(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        self.__setup_ui()
        self.__connect_slot()

    def __setup_ui(self):
        self.setTabsClosable(True)
        self.setIconSize(QSize(15,15))
        self.setStyleSheet('QTabBar::close-button{image:url(./icon/close/close_red.png);}')


    def add_tab(self, con_key, table_name, tab_color):
        widget = DataItemWidget(con_key, table_name)
        self.addTab(widget, table_name)
        self.setCurrentWidget(widget)

        icon_path = IconManager().get_close_icons(tab_color)
        btn = TabBtn(icon_path)
        index = self.currentIndex()
        self.tabBar().setTabButton(index, QTabBar.LeftSide,btn)
        self.connect(btn,SIGNAL('clicked()'),self,SLOT('__on_close_btn()'))

        #index = self.currentIndex()
        #self.setTabIcon(index,QIcon('./icon/label/label_blue.png'))

    def __connect_slot(self):
        #self.connect(self,SIGNAL('tabCloseRequested (int)'), self, SLOT('__on_tab_close(int)'))
        pass

    @pyqtSlot()
    def __on_close_btn(self):
        btn = self.sender()
        tab_count = self.tabBar().count()
        for i in range(tab_count):
            tab_btn = self.tabBar().tabButton(i,QTabBar.LeftSide)
            if btn is tab_btn:
                self.removeTab(i)
                return

